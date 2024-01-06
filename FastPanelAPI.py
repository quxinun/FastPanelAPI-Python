import requests
from requests.exceptions import RequestException
from fake_useragent import UserAgent
import paramiko
import re
from FastPanelAPI.Logger import logger

class FastPanelAPI:
    def __init__(self, fastlogin: str, fastpassword: str, fastpanel_ip_port: str, remote_ip: str, remote_port: int, remote_username: str, remote_password: str, user_agent: str=UserAgent().random) -> None:
        self.__fastlogin = fastlogin
        self.__fastpassword = fastpassword
        self.__user_agent = user_agent
        self.__fastpanel_ip_port = fastpanel_ip_port
        self.__remote_ip = remote_ip
        self.__remote_port = remote_port
        self.__remote_username = remote_username
        self.__remote_password = remote_password
        
        self.__session = requests.Session()
        self.__session.verify = False

        try:
            response = self.__session.post(
                f"https://{self.__fastpanel_ip_port}/login",
                json={"username": self.__fastlogin, "password": self.__fastpassword},
                headers={"user-agent": self.__user_agent}
            )

            response.raise_for_status()

            response_json = response.json()
            self.__token = response_json.get("token")
            
            logger.info("Successful authentication")
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication error: {e}")


    def __execute_ssh_command(self, command: str):
        ssh = paramiko.SSHClient()

        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.__remote_ip, port=self.__remote_port, username=self.__remote_username,
                        password=self.__remote_password)
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read().decode('utf-8')
            return result
        except Exception as e:
            logger.error(f"Error connecting to the server: {e}")
        finally:
            ssh.close()


    def create_mail(self, name: str, password: str, domain: str):
        if len(password) < 8 or not any(char.isdigit() for char in password) or password.islower() or password.isupper():
            logger.error("Error: The password must contain at least 8 characters, at least one digit and have different registers.")
        else:
            if not re.match("^[a-zA-Z0-9]+$", name):
                logger.error("Mistake: The name contains invalid characters.")
            else:
                try:
                    result = self.__execute_ssh_command(
                        f"""mogwai emails domains list | grep {domain} | awk '{{print $1}}'""")
                    try:
                        id = int(result)
                        try:
                            response = self.__session.post(
                                f"https://{self.__fastpanel_ip_port}/api/email/domains/{id}/boxs",
                                json={
                                    "login": name,
                                    "password": password,
                                    "quota": 0,
                                    'redirects': [],
                                    'save_in_box': False,
                                    'aliases': [],
                                    'spam_to_junk': False,
                                },
                                headers={
                                    "authorization": f"Bearer {self.__token}",
                                    "user-agent": self.__user_agent
                                }
                            )

                            if response.status_code == 201:
                                logger.info(f"Successfully created the mail {name}@{domain}")
                            else:
                                logger.warning(f"{name}@{domain} is already occupied.")

                        except RequestException as e:
                            logger.error(f"Request execution error: {e}")
                        except Exception as e:
                            logger.error(f"An unexpected error occurred: {e}")

                    except:
                        logger.warning("There is no mail with this name and domain.")
                except Exception as e:
                    logger.error(e)


    def delete_mail(self, email: str):
        try:
            name = email.strip().split('@')[0]
            domain = email.strip().split('@')[1]
        except:
            logger.error("Enter the data in the format: name@domain.ru")

        try:
            result = self.__execute_ssh_command(
                f"""mogwai emails boxes list --domain {domain} | grep "{name}@{domain}" | awk '{{print $1}}'""")
            try:
                id = int(result)
                try:
                    response = self.__session.delete(f"https://{self.__fastpanel_ip_port}/api/mail/box/{id}",
                                              headers={"authorization": f"Bearer {self.__token}",
                                                       "user-agent": self.__user_agent})
                    if response.status_code == 200:
                        logger.info(f"Successfully deleted the mail {email}")
                    else:
                        logger.warning(f"Couldn't delete mail {email}")
                except Exception as e:
                    logger.error(f"Request error: {e}")
            except:
                logger.warning("There is no mail with this name and domain.")
        except Exception as e:
            logger.error(e)


    def change_password(self, email: str, newpassword: str):
        if len(newpassword) < 8 or not any(char.isdigit() for char in newpassword) or newpassword.islower() or newpassword.isupper():
            logger.error("Error: The password must contain at least 8 characters, at least one digit and have different registers.")
        else:
            try:
                name = email.strip().split('@')[0]
                domain = email.strip().split('@')[1]
            except:
                logger.error("Enter the data in the format: name@domain.ru")

            try:
                result = self.__execute_ssh_command(
                    f"""mogwai emails boxes list --domain {domain} | grep "{name}@{domain}" | awk '{{print $1}}'""")
                try:
                    id = int(result)
                    try:
                        response = self.__session.put(f"https://{self.__fastpanel_ip_port}/api/mail/box/{id}",
                                                headers={"authorization": f"Bearer {self.__token}",
                                                        "user-agent": self.__user_agent},
                                                        json={"password": f"{newpassword}"})
                        if response.status_code == 200:
                            logger.info(f"Successfully changed the password of {email}")
                        else:
                            logger.warning(f"Couldn't change the password for {email}")
                    except Exception as e:
                        logger.error(f"Request error: {e}")
                except:
                    logger.warning("There is no mail with this name and domain.")
            except Exception as e:
                logger.error(e)