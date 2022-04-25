# LineAlghoraires
- Inputs : 
  - A "preferences" file which contains the individual preferences of students regarding each time slot
  - A "format" file which contains the format of the session : the number of students accepted for each slot
- Output : 
  - A "Schedule" file
  - A "Student and date" file which maps every student to its given date


## How to make it work
- First of all, make sure to have Poetry installed, updated and well configured.

- Then, install the dependencies : `poetry install`

- Add your "preferences" and "format" files in the `data` folder and make sure the name is adapted in the code.

- Run with `poetry run python main.py`

## Poetry modules 
- pandas
- PuLP
- numpy
- dateutil
- To display as html file : `pandas`
- To convert html to pdf : `pdfkit`
## External dependencies
- Install GLPK (to solve the problem)
- Install wkhtmltopdf (for display purpose)

### Ubuntu/Debian
`sudo apt-get install wkhtmltopdf glpk`
### Arch
`sudo pacman -S wkhtmltopdf glpk`
