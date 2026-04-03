import re
import requests
import csv
import sys
from PIL import Image
from io import BytesIO

from bs4 import BeautifulSoup
from PDF import PDF
from requests.exceptions import RequestException

puzzle_store_urls = {
    "buffalo": "https://buffalogames.com/sale/",
    "ravensburger": "https://www.ravensburger.us/en-US/products/sale/sale-puzzles"
}


def main():
    user_input = input("Would you like to find sale puzzles on Buffalo, Ravensburger, or both? ").lower().strip()
    while True:
        if user_input not in ["buffalo", "ravensburger", "both"]:
            user_input = input("Would you like to find sale puzzles on Buffalo, Ravensburger, or both? ").lower().strip()
        else:
            break
    if user_input == "buffalo":
        sale_page_urls = get_sale_puzzle_info({k: v for k, v in puzzle_store_urls.items() if k == "buffalo"})
    elif user_input == "ravensburger":
        sale_page_urls = get_sale_puzzle_info({k: v for k, v in puzzle_store_urls.items() if k == "ravensburger"})
    elif user_input == "both":
        sale_page_urls = get_sale_puzzle_info(puzzle_store_urls)

    
    store_puzzle_info(sale_page_urls)
    PDF.create_puzzle_sales_pdf()


def get_sale_puzzle_info(urls):
    if not urls:
        sys.exit("something went wrong:(")
    sale_puzzles = []
    for website in urls:
        counter = 1
        ## for ALL sale puzzle pages - you will get ~50 pages of puzzles
        # while True:
        ## for just the first pages of each website
        while counter < 2:
            try:
                page = requests.get(urls[website] ,params=f"page={counter}", timeout=10)
            except requests.exceptions.RequestException as e:
                print(e)
            soup = BeautifulSoup(page.content, "html.parser")

            if website == "buffalo":
                puzzle_products_buffalo = soup.find_all(class_="product")
                sale_puzzles.append(puzzle_products_buffalo)
                no_next_page = soup.find(class_="pagination-item pagination-item--next")
                if not no_next_page or counter == 10:
                    break
            if website == "ravensburger":
                puzzle_products_ravensburger = soup.find_all(class_="col-6 col-md-3")
                sale_puzzles.append([product for product in puzzle_products_ravensburger if product.find(class_="price strike")])
                if counter > 1 or counter == 10:
                    next_page_disabled = soup.find(class_="btn btn-primary btn-icon disabled")
                    if next_page_disabled:
                        break

            counter += 1
    return sale_puzzles


def store_puzzle_info(products):
    if not products:
        sys.exit("something went wrong:(")
    try:
        with open("list_of_puzzles.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "img", "url", "piece_count", "original_price", "discount_price", "discount_percentage"])
            writer.writeheader()

            for website in products:
                for puzzle in website:
                    puzzle_dict = {}
                    puzzle_dict["name"] = find_puzzle_name(puzzle)
                    puzzle_dict["img"] = get_puzzle_img(puzzle)
                    puzzle_dict["url"] = puzzle.find('a')['href']
                    puzzle_dict["piece_count"] = get_piece_count(puzzle_dict["name"])
                    puzzle_dict["original_price"] = get_puzzle_original_price(puzzle)
                    puzzle_dict["discount_price"] = get_puzzle_discount_price(puzzle)
                    puzzle_dict["discount_percentage"] = get_puzzle_discount_percentage(puzzle)
                    writer.writerow(puzzle_dict)
    except OSError:
        sys.exit("something went wrong with the file")


def get_puzzle_img(puzzle):
    get_url = puzzle.find('img')['data-src']

    if not get_url:
        return "ravensburger_images/placeholder_image.png"
    
    if ".webp" in get_url:
        matches = re.search(r"[Ravensburger|Jigsaw]-(.*)-", get_url)
        if matches:
            img_name = matches[0]
        else:
            img_name = f"{puzzle}"

        try:
            request_img = requests.get(get_url, timeout=10).content
        except requests.exceptions.RequestException as e:
            print(e)

        img = Image.open(BytesIO(request_img)).convert("RGB")
        img_name = f"ravensburger_images/{img_name}.jpg"
        img.save(img_name)
        return img_name
    else:
        return get_url


def find_puzzle_name(puzzle):
   buffalo = puzzle.find(class_='card-title')
   if not buffalo:
       ravensburger = puzzle.find('a', class_="card-product-name")
       if not ravensburger:
           return "Name Not Found"
       return ravensburger.find('span').text.strip()
   else:
       return buffalo.text.strip()


def get_puzzle_original_price(puzzle):
    original_price = puzzle.find(class_=["price price--non-sale", "price strike"])

    if original_price:
        return original_price.text.strip()
    return "no original price"


def get_puzzle_discount_price(puzzle):
    buffalo = puzzle.find(class_="price price--withoutTax")
    ravensburger = puzzle.find(class_="card-price price reduce")

    if ravensburger:
        remove_original_price = ravensburger.select("div:not(.price strike)")[0]
        return remove_original_price.find('div', class_=None).text.strip()

    if buffalo:
        return buffalo.text.strip()
    return "no discount price rude"


def get_puzzle_discount_percentage(puzzle):
    percentage = puzzle.find(class_=["sale-text", "badge percent"])

    if percentage:
        percentage_text = percentage.text.strip()

        if "-" in percentage_text:
            return f"{percentage_text[1:]} Off"
        else:
            return percentage_text
    return "discount percentage not found"


def get_piece_count(name):
    matches = re.search(r"(\d{2,4})", name, re.IGNORECASE)
    if matches:
        return f"{matches[1]} Pieces"
    return "piece count unavailable"


if __name__ == "__main__":
    main()