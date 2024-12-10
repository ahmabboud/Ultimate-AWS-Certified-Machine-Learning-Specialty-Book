
# **Ultimate AWS Certified Machine Learning Specialty MLS-C01 Exam Guide - Repository**

Welcome to the **Ultimate AWS Certified Machine Learning Specialty MLS-C01 Exam Guide** repository! This repository contains all the necessary resources, scripts, datasets, and instructions for the hands-on labs in the book. By following this guide, you'll set up your environment to interact with AWS services and gain practical experience replicating real-world scenarios.

Use this guide to prepare your computer, connect to AWS, and set up your development environment to complete the labs provided in this repository.

---

## **Repository Structure**

This repository is organized by chapters to help you navigate through the labs and resources:

```
Ultimate-AWS-Certified-Machine-Learning-Specialty-Book/
├── ch1/                     # Chapter 1 materials
├── ch2/                     # Chapter 2 materials
│   ├── datasets/            # Datasets for Chapter 2 labs
│   ├── scripts/             # Python scripts for Chapter 2 labs
│   └── README.md            # Chapter-specific guide
├── ch3/                     # Chapter 3 materials
├── ...                      # Additional chapters
└── README.md                # General repository overview (this file)
```

Each chapter contains:
- **Datasets**: Sample data needed for the labs.
- **Scripts**: Python scripts to interact with AWS services.
- **Instructions**: Detailed step-by-step lab instructions.
- **requirements.txt**: Chapter-specific Python dependencies, if applicable.

---

## **What You'll Need**

Before starting, make sure you have the following:
1. A computer with **Windows**, **macOS**, or **Linux**.
2. An **AWS account** with sufficient permissions to create and use AWS resources (e.g., S3, Lambda, Glue).
3. **Python 3.x** installed.
4. Basic familiarity with using a terminal/command prompt.

---

## **Step 1: Set Up Visual Studio Code**

You’ll use **Visual Studio Code (VS Code)** as your primary code editor. It’s lightweight, beginner-friendly, and integrates well with AWS through the **AWS Toolkit**.

1. Download **VS Code** from the [official website](https://code.visualstudio.com/).
2. Install VS Code by following the instructions for your operating system.
3. Once installed, open VS Code.

---

## **Step 2: Install AWS Toolkit for Visual Studio Code**

The **AWS Toolkit** is an extension for VS Code that makes it easy to interact with AWS services directly from your code editor.

### Install the AWS Toolkit:
1. Open VS Code.
2. Click the **Extensions** icon in the left sidebar (or press `Ctrl+Shift+X` on Windows/Linux or `Cmd+Shift+X` on macOS).
3. In the Extensions view, search for **AWS Toolkit**.
4. Click **Install** to add the AWS Toolkit extension.

---

## **Step 3: Create an AWS Account**

If you don’t already have an AWS account, follow these steps:

1. Go to the [AWS Free Tier page](https://aws.amazon.com/free/) and click **Create a Free Account**.
2. Follow the instructions to create your account:
   - Provide your email address and create a password.
   - Enter your payment information (required for the free tier, but you won’t be charged for free-tier usage).
   - Verify your phone number and select the **Basic Support Plan** (free).
3. After signing up, log in to the [AWS Management Console](https://aws.amazon.com/console/).

---

## **Step 4: Set Up AWS Credentials**

To allow AWS Toolkit or CLI tools to interact with your AWS account, you need AWS **Access Key ID** and **Secret Access Key**. These credentials are tied to an IAM user in your account.

### **Step 4.1: Create an IAM User**
1. Go to the [IAM Console](https://console.aws.amazon.com/iam/).
2. Click **Users** in the sidebar, then click **Add Users**.
3. Enter a **User name** (e.g., `aws-beginner`).
4. Select **Programmatic access** under **Access type**.
5. Click **Next: Permissions** and assign a policy:
   - For beginners, attach the **AdministratorAccess** policy (this provides full access to AWS resources).
6. Click **Next: Review**, then click **Create user**.
7. On the success page, you’ll see the **Access Key ID** and **Secret Access Key**.
   - **Important**: Download the `.csv` file or copy these credentials. You won’t be able to view the **Secret Access Key** again.

---

### **Step 4.2: Configure AWS Toolkit with Your Credentials**
1. Open the **AWS Explorer** in VS Code by clicking the **AWS icon** in the sidebar.
2. Click **Connect to AWS** in the AWS Explorer.
3. Select **Add a new profile to your AWS credentials file**.
4. Enter the following details:
   - **Profile name**: Choose a name (e.g., `default` or `aws-beginner`).
   - **Access Key ID**: Paste the key from the IAM user you created.
   - **Secret Access Key**: Paste the key from the IAM user you created.
   - **Default region**: Choose your preferred AWS region (e.g., `us-east-1`).

---

## **Step 5: Clone the Repository**

Now that your AWS Toolkit is set up, clone this repository to your computer.

1. Open a terminal (or the integrated terminal in VS Code).
2. Navigate to the folder where you want to store this repository:
   ```bash
   cd ~/Documents
   ```
3. Clone the repository:
   ```bash
   git clone https://github.com/ahmabboud/Ultimate-AWS-Certified-Machine-Learning-Specialty-Book.git
   ```
4. Navigate into the repository folder:
   ```bash
   cd Ultimate-AWS-Certified-Machine-Learning-Specialty-Book
   ```

---

## **Step 6: Set Up a Python Virtual Environment**

Python is used throughout this repository. To keep your environment clean and organized, we’ll use a **single virtual environment for the entire repository**.

1. Create a virtual environment in the root of the repository:
   ```bash
   python3 -m venv venv
   ```
   This will create a folder named `venv` in the repository.

2. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```

3. Install dependencies for the entire repository:
   - If a global `requirements.txt` is provided in the root folder:
     ```bash
     pip install -r requirements.txt
     ```
   - Otherwise, combine chapter-specific dependencies by installing each `requirements.txt` from all chapter folders:
     ```bash
     for req_file in */requirements.txt; do pip install -r $req_file; done
     ```

4. Verify the installation:
   ```bash
   pip list
   ```


## **Troubleshooting**

### **Problem: AWS Toolkit Cannot Connect**
- Double-check your AWS credentials and region in the AWS Explorer.
- Ensure your IAM user has the necessary permissions (e.g., `AdministratorAccess`).

### **Problem: Python Script Fails**
- Confirm that you activated the virtual environment (`venv`).
- Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### **Problem: Missing `git` or `python3`**
- Install `git` and Python using your system's package manager:
  - **macOS**:
    ```bash
    brew install git python
    ```
  - **Ubuntu/Debian**:
    ```bash
    sudo apt update
    sudo apt install git python3
    ```

---

## **Next Steps**

With your environment set up, you’re ready to dive into the labs. Navigate to the chapter folders, follow the `README.md` and instructions provided, and start experimenting with AWS services. Happy learning! 🚀