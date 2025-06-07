# apollo-scraper
HackMIT's CR email scraper using the Apollo API!

## Prerequisites
**Python `>3.6`**

Run the following commands to check your currently installed versions:
```sh
$ python --version
```

Download the latest release here: https://www.python.org/downloads/

## Usage
1. Clone the repository:
```sh
$ git clone https://github.com/techx/apollo-scraper.git
```
2. Add your Apollo API Key (from go/accounts) to the .env file.
3. Download your company list as a .csv file (you should have one column of company names with "Company" as the header). 
4. Run the following command:
```sh
$ python main.py
```
5. Input the directory path to your file and then the file name as prompted (be sure to include the .csv file extension in the name).
6. Sit back and wait!

## License
[MIT](https://choosealicense.com/licenses/mit/)