from selenium import webdriver

from prog_hub_parser import ProhHubParser


def main():
  try:
    driver = webdriver.Chrome()
    parser = ProhHubParser(driver, "python")
    parser.parse()
  except Exception as err:
    print(err)


if __name__ == "__main__":
  main()
