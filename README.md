# FastPanelAPI

FastPanelAPI is a Python library for interacting with FastPanel, providing functions to manage email accounts. This API allows you to create, delete, and change passwords for email accounts on your FastPanel server.

## Installation

To use the FastPanelAPI, follow these steps:

1. Install the required dependencies:

   ```bash
   pip install requests paramiko fake_useragent
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/quxinu/FastPanelAPI-Python.git
   ```

## Usage

To use the FastPanelAPI in your project, follow these steps:

1. Import the FastPanelAPI class from the library:

   ```python
   from FastPanelAPI import FastPanelAPI
   ```

2. Initialize the FastPanelAPI class with your FastPanel login credentials and server details:

   ```python
   fast_api = FastPanelAPI(
       fastlogin="your_fastpanel_login",
       fastpassword="your_fastpanel_password",
       fastpanel_ip_port="your_fastpanel_ip:your_fastpanel_port",
       remote_ip="your_remote_server_ip",
       remote_port=your_remote_server_port,
       remote_username="your_remote_server_username",
       remote_password="your_remote_server_password"
   )
   ```

3. Use the provided functions to interact with FastPanel:

   - To create a new email account:

     ```python
     fast_api.create_mail(name="email_username", password="email_password", domain="email_domain")
     ```

   - To delete an existing email account:

     ```python
     fast_api.delete_mail(email="email_to_delete@example.com")
     ```

   - To change the password of an existing email account:

     ```python
     fast_api.change_password(email="email_to_change@example.com", newpassword="new_password")
     ```

## Example

```python
from FastPanelAPI import FastPanelAPI

fast_api = FastPanelAPI(
    fastlogin="your_fastpanel_login",
    fastpassword="your_fastpanel_password",
    fastpanel_ip_port="your_fastpanel_ip:your_fastpanel_port",
    remote_ip="your_remote_server_ip",
    remote_port=your_remote_server_port,
    remote_username="your_remote_server_username",
    remote_password="your_remote_server_password"
)

fast_api.create_mail(name="john_doe", password="secure_password123", domain="example.com")
fast_api.delete_mail(email="john_doe@example.com")
fast_api.change_password(email="john_doe@example.com", newpassword="new_secure_password456")
```