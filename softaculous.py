"""
Python Library for Softaculous API

https://www.softaculous.com/docs/API

Author: Benton Snyder
Website: http://bensnyde.me
Created: 1/4/15

"""
from phpserialize import *
import logging
import base64
import httplib
import json
import socket

class Softaculous:
    def __init__(self, cp_base_url, cp_username, cp_password):
        """Constructor

        Parameters
            cp_base_url: str softaculous's control panel base url (ex. cpanel.example.com)
            cp_username: str softaculous's control panel username
            cp_password: str softaculous's control panel password
        Returns
            None
        """
        self.base_url = cp_base_url
        self.username = cp_username
        self.password = cp_password

    def __softaculous_api_query(self, kwargs=None):
        """Query Softaculous API

        Parameters
            kwargs:
        Returns:
            json response from server
        """
        try:
            query_string = "/frontend/x3/softaculous/index.live.php?&api=serialize"
            http_verb = "GET"

            if kwargs:
                http_verb = "POST"
                for key,val in kwargs.items():
                    query_string += "&"+key+"="+val

            print query_string

            conn = httplib.HTTPSConnection(self.base_url, 2083)
            conn.request(http_verb, query_string, headers={'Authorization':'Basic ' + base64.b64encode(self.username+':'+self.password).decode('ascii')})
            response = conn.getresponse()
            data = loads(response.read())
            conn.close()

            return data
        except httplib.HTTPException as ex:
            logging.critical("HTTPException from Softaculous API: %s" % ex)
        except socket.error as ex:
            logging.critical("Socket.error connecting to Softaculous API: %s" % ex)
        except ValueError as ex:
            logging.critical("ValueError decoding Softaculous API response string: %s" % ex)
        except Exception as ex:
            logging.critical("Unhandled Exception while querying Softaculous API: %s" % ex)
        return False

    def list_scripts(self):
        """List Scripts

            https://www.softaculous.com/docs/API#List_Scripts

        Parameters
            None
        Returns
            JSON
                time_taken: float
                timenow: int epoch timestamp
                title: str
                top: dict
                    int: float
                iscripts: dict
                    int(script_id): dict
                        cat: str category
                        desc: str description
                        ins: int
                        name: str human friendly name
                        softname: str software friendly name
                        type: str php|js|perl
                        ver: str version

        """
        data = {
            "act": None
        }

        return self.__softaculous_api_query(data)

    def install_script(self, script_id, **kwargs):
        """Install Script

            https://www.softaculous.com/docs/API#Install_a_Script

        Parameters
            script_id: str script id
            *kwargs:
                softsubmit: int triggers the installation routine [1]
                softdomain: str
                softdirectory: str subdirectory to install script into (blank for root of domain)
                softdb: str database name
                dbusername: str database user
                dbuserpass: str database user's password
                hostname: str MySQL server hostname
                admin_username: str admin account name
                admin_pass: str admin account password
                admin_email: str admin account email
                language: str language [en|es|etc...]
                site_name: str site name
                site_desc: str site description
        Returns
            JSON
                title: str
                info: dict
                    overview:
                    demo:
                    ratings:
                    support:
                    release_date:
                    mod:
                    mod_files:
                    import:
                settings:
                    Site Settings: dict
                        license_key:
                            tag:
                            head:
                            exp:
                            handle:
                            optional:
                        admin_fname:
                            tag:
                            head:
                            exp:
                            handle:
                            optional:
                        admin_lname:
                            tag:
                            head:
                            exp:
                            handle:
                            optional:
                dbtype:
                __settings:
                    adminurl:
                installations: dict
                notes:
                cron:
                datadir:
                overwrite_option:
                protocols:
                    int: str
                nopackage:
                theme_package:
                timenow:
                time_taken

        """
        data = {
            "act": "software",
            "soft": script_id,
        }

        return self.__softaculous_api_query(data)

    def upgrade_script(self, installation_id):
        """Upgrade Script

            https://www.softaculous.com/docs/API#Upgrade_an_Installed_Script

        Parameters
            installation_id: str installation id
        Returns
            JSON
        """
        data = {
            "act": "upgrade",
            "insid": installation_id,
        }

        return self.__softaculous_api_query(data)

    def remove_script(self, installation_id):
        """Remove Script

            https://www.softaculous.com/docs/API#Remove_an_Installed_Script

        Parameters
            installation_id: str installation id
        Returns
            JSON
        """
        data = {
            "act": "remove",
            "insid": installation_id,
        }

        return self.__softaculous_api_query(data)

    def import_installation(self, script_id):
        """Import Installation

            https://www.softaculous.com/docs/API#Import_an_Installation

        Parameters
            script_id: str script id
        Returns
            JSON
        """
        data = {
            "act": "import",
            "soft": script_id,
        }

        return self.__softaculous_api_query(data)

    def list_installed_scripts(self, show_only_installations_with_updates_available=False):
        """List Installed Scripts

            https://www.softaculous.com/docs/API#List_Installed_Script

        Parameters
            show_only_installations_with_updates_available: bool
        Returns
            JSON
                time_taken:
                timenow:
                title:
                installations: dict
        """
        data = {
            "act": "installations",
            "showupdates": ("false", "true")[show_only_installations_with_updates_available],
        }

        return self.__softaculous_api_query(data)

    def list_backups(self):
        """List Backups

            https://www.softaculous.com/docs/API#List_Backups

        Parameters
            None
        Returns
            JSON
        """
        data = {
            "act": "backups"
        }

        return self.__softaculous_api_query(data)

    def backup_installed_script(self, installation_id):
        """Backup an Installed Script

            https://www.softaculous.com/docs/API#Backup_an_Installed_Script

        Parameters
            installation_id: str installation id
        Returns
            JSON
        """
        data = {
            "act": "backup",
            "insid": installation_id,
        }

        return self.__softaculous_api_query(data)

    def restore_installed_script(self, back_file_name):
        """Restore an Installed Script

            https://www.softaculous.com/docs/API#Restore_an_Installed_Script

        Parameters
            None
        Returns
            JSON
        """
        data = {
            "act": "restore",
            "restore": backup_filename
        }

        return self.__softaculous_api_query(data)

    def download_backups(self, backup_filename):
        """Download Backups

            https://www.softaculous.com/docs/API#Download_Backups

        Parameters
            backup_filename: str backup filename to download
        Returns
            JSON
        """
        data = {
            "act": "backups",
            "download": backup_filename,
        }

        return self.__softaculous_api_query(data)

    def delete_backup(self, backup_filename):
        """Delete Backup

            https://www.softaculous.com/docs/API#Delete_Backups

        Parameters
            backup_filename: str backup filename to delete
        Returns
            JSON
        """
        data = {
            "act": "backups",
            "remove": backup_filename,
        }

        return self.__softaculous_api_query(data)
