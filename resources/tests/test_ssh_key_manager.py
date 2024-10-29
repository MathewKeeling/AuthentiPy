import os
import pytest
import yaml
from unittest.mock import patch, mock_open
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
from ssh_key_manager import (
    generate_ssh_key,
    read_servers,
    is_key_present,
    copy_public_key,
    verify_ssh_access,
)

# Mock data
mock_servers = {
    "server1": {"fqdn": "server1.example.com", "service_account": "user1"},
    "server2": {"fqdn": "server2.example.com", "service_account": "user2"},
}


@pytest.fixture
def mock_yaml_file():
    return yaml.dump({"servers": mock_servers})


def test_generate_ssh_key(mocker):
    mocker.patch("os.path.isfile", return_value=False)
    mocker.patch("os.system")
    generate_ssh_key()
    os.system.assert_called_once_with(
        "ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa"
    )


def test_generate_ssh_key_exists(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    mocker.patch("os.system")
    generate_ssh_key()
    os.system.assert_not_called()


def test_read_servers(mocker, mock_yaml_file):
    mocker.patch("builtins.open", mock_open(read_data=mock_yaml_file))
    servers = read_servers("dummy_path")
    assert servers["servers"] == mock_servers


def test_is_key_present(mocker):
    mock_connection = mocker.patch("ssh_key_manager.ConnectHandler")
    mock_connection.return_value.send_command.return_value = ""
    assert is_key_present("server1.example.com", "user1") is True


def test_is_key_present_not_found(mocker):
    mock_connection = mocker.patch("ssh_key_manager.ConnectHandler")
    mock_connection.return_value.send_command.return_value = "not found"
    assert is_key_present("server1.example.com", "user1") is False


def test_is_key_present_exception(mocker):
    mock_connection = mocker.patch(
        "ssh_key_manager.ConnectHandler", side_effect=NetmikoTimeoutException
    )
    assert is_key_present("server1.example.com", "user1") is False


def test_copy_public_key(mocker):
    mocker.patch("ssh_key_manager.is_key_present", return_value=False)
    mock_connection = mocker.patch("ssh_key_manager.ConnectHandler")
    mocker.patch("tqdm.tqdm")
    copy_public_key(mock_servers)
    assert mock_connection.call_count == 2


def test_verify_ssh_access(mocker):
    mock_connection = mocker.patch("ssh_key_manager.ConnectHandler")
    mock_connection.return_value.send_command.return_value = (
        "SSH to server1.example.com successful"
    )
    mocker.patch("tqdm.tqdm")
    verify_ssh_access(mock_servers)
    assert mock_connection.call_count == 2
