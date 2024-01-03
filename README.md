# Pittsburgh MTA Train System

Train system simulation project for ECE 1140 Fall 2023.

### Sub-System Modules:

| Team Member | Role |
| :---: | :---: |
| Julia Koma | CTC Office |
| Asher Goodwin | Track Controller |
| Ralph Gonsalves | Track Model |
| Aidan Gresko | Train Model |
| Beryl Sin | Train Controller (SW) | 
| Reed Yulis | Train Controller (HW) |

# Installation Guide
> [!TIP]
> Please refer to the documentation for further help

1) Clone the Repository:
```
git clone https://github.com/ralphg1002/Pittsburgh-MTA.git
```
2) Install and setup poetry (Refer to the poetry guide in the documentation for help)

3) Install the package dependencies:
```
poetry install
```

# Running the Application

To run the application, run the following command from the root:
```
poetry run python src/main/main.py
```

> [!NOTE]
> The recommended display settings for the application is a 125% scale and a 1920 x 1080 display resolution**