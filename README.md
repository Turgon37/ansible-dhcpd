Ansible Role DHCP Daemon
========

[![Build Status](https://travis-ci.org/Turgon37/ansible-dhcpd.svg?branch=master)](https://travis-ci.org/Turgon37/ansible-dhcpd)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-Turgon37.dhcpd-blue.svg)](https://galaxy.ansible.com/Turgon37/dhcpd/)

## Description

:grey_exclamation: Before using this role, please know that all my Ansible roles are fully written and accustomed to my IT infrastructure. So, even if they are as generic as possible they will not necessarily fill your needs, I advice you to carrefully analyse what they do and evaluate their capability to be installed securely on your servers.

:warning: This role is under development, some important (and possibly breaking) changes may happend. Don't use it in production level environments but you can eventually base your own role on this one :hammer:

This roles configures an instance of DHCP daemon.
Supports multi instances of daemon.

## Requirements

Require Ansible >= 2.4

### Dependencies

* systemd service manager

## OS Family

This role is available for Debian

## Features

At this day the role can be used to :

  * install dhcp daemon
  * configure following objects using plain text files
    * subnets
    * hosts
    * groups
    * pools
    * options declarations
    * OMAPI configuration
    * secret keys (with automatic random secret generation available)
  * configure LDAP backend
  * [local facts](#facts)

## Configuration

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below. To see default values please refer to this file.

### Global

| Name                  | Types/Values     | Description                                                                                |
| ----------------------| -----------------|------------------------------------------------------------------------------------------- |
| dhcpd__facts          | Boolean          | Install the local fact script                                                              |
| dhcpd__service_enabled| Boolean          | Enable or not the service                                                                  |
| dhcpd__instances      | Dict of instance | See below                                                                                  |

### Instance

This role allow multiple instance of DHCP daemon to be configured. Each instance have it's own configuration, own leases database file and secret keys set.
Use `dhcpd__instances` dict to declare each instance.
Each of theses one must be set under a unique key name and accept the following parameters.

| Name              | Types/Values  | Description                                                                                |
| ------------------| --------------|------------------------------------------------------------------------------------------- |
| mode              | String        | Choose dhcpd configuration mode in 'files' or 'ldap'. (See below for mode specific options)|
| listen_interfaces | List of String| List of interface on which dhcpd will listen for DHCP requests.                            |
| ip_version        | Integer       | Version of IP protocol to enable in DHCP daemon. Must be in 4, 6                           |
| daemon_options    | String        | Optional additionnals daemon options                                                       |

### Mode FILES

| Name          | Types/Values             | Description                                                   |
| --------------| -------------------------|-------------------------------------------------------------- |
| authoritative | Boolean                  | Boolean that make this DHCP server authoritative (not a relay)|
| parameters    | List of String           | Dhcp parameters in raw string format to apply on configuraton |
| dhcp_options  | Dict of String           | Dhcp option in "key: value" format                            |
| subnets       | List of Subnet statements| Declare subnets                                               |
| hosts         | List of Host statements  | Hosts entries at the root of the configuration                |
| secret_keys   | List of key statements   | List of secret keys to configure (see below)                  |
| omapi_enabled | Boolean                  | Enable (open) or not the OMAPI                                |
| omapi_port    | Integer                  | Port of OMAPI interface                                       |

Note for *dhcp_options*, some parameters need to be enclosed by quotes in the final configuration file, this role comes with a list of theses options (dhcpd__quoted_dhcp_options_name) and apply automatically the quotes. So, normally you do not have to put theses quotes in inventory files.

#### Key statements

Ansible manage the list of secret keys declared for DHCPD. Each key item must be set in the dhcpd__keys dict, see below two examples:

```
dhcpd__instances:
  4:
    secret_keys:
      key1:
        algorithm: hmac-sha1
        secret: XXXXXXXX==
      ddns:
        algorithm: hmac-md5
        # secret will be autogenerate on first run
```

If you do not provide the 'secret' key, it will be auto generated (only at first Ansible playbook run) according the selected algorithm.
Please take care that only algorithm declared in the internal role setting 'dhcpd__keys_size_mapping' will be accepted.

:information_source: If you enable OMAPI with dhcpd__omapi_enabled, a key will be automatically produced for it.


#### Host statement

A host statement must be in the following format

```
- name: host1
  mac_address: ee:ee:ee:ee:ee:ee
  ipv4_address: 192.168.1.1
  deny: False
```

#### Subnet statement

A subnet statement must be in the following format

```
- network: 10.0.0.0
  netmask: 255.255.255.0
  range: 10.0.0.1 10.0.0.10
  parameters: # Raw parameters
    ...
  dhcp_options:  # dhcp options
    routers: 10.51.57.254
    ...
  pools:  # pool statements
    ...
  groups: # groups statements
    ...
  hosts:  # host statements
    ...
```

#### Pool statement

A pool statement must be in the following format

```
- range: 10.0.0.1 10.0.0.10
  parameters: # Raw parameters
    ...
  dhcp_options:  # dhcp options
    ...
  groups: # groups statements
    ...
  hosts:  # host statements
    ...
```

#### Groups statement

A group statement must be in the following format

```
- parameters: # Raw parameters
    ...
  dhcp_options:  # dhcp options
    ...
  groups: # groups statements
    ...
  hosts:  # host statements
    ...
```


### Mode LDAP

| Name            | Types/Values | Description                                                                                         |
| --------------- |--------------|-----------------------------------------------------------------------------------------------------|
| ldap_server     | String       | The ip address/domain name of the LDAP server                                                       |
| ldap_port       | Integer      | The port to use to bind with LDAP server                                                            |
| ldap_username   | String       | OPTIONAL bind username/dn                                                                           |
| ldap_password   | String       | OPTIONAL bind password                                                                              |
| ldap_basedn     | String       | LDAP base DN of the DHCP tree                                                                       |
| ldap_servercn   | String       | The commonname (cn= field) of the DhcpServer entry to use. (default is to use the fqdn of this host)|
| ldap_method     | String       | The LDAP query method, 'static' or 'dynamic'                                                        |
| ldap_debug_file | String       | OPTIONAL The debug file in which dhcpd will dump read LDAP configuration                            |

## Facts

By default the local fact are installed and expose the following variables :


* ```ansible_local.dhcpd.version_full```
* ```ansible_local.dhcpd.version_major```

## Example

### Playbook

Use it in a playbook as follows:

```yaml
- hosts: all
  roles:
    - turgon37.dhcpd
```

### Inventory

To use this role create or update your playbook according the following examples :

  * Exemple of configuration with classical FILES backend

```
dhcpd__instances:
  4:
    mode: files
    listen_interfaces: wlan0
    parameters:
      - default-lease-time 864000
      - deny bootp
      - ddns-updates off
      - ddns-update-style none
      - log-facility local7
    subnets:
      - network: 10.0.0.0
        netmask: 255.255.255.0
        range: 10.0.0.1 10.0.0.10
        dhcp_options:
          routers: 10.0.0.254
          broadcast-address: 10.0.0.255
          domain-name: 'local'
          domain-name-servers: 10.0.0.254
        hosts:
          - name: host1
            mac_address: ee:ee:ee:ee:ee:e
            ipv4_address: 10.0.0.1
```

  * A complexe example with pool and group


  * Exemple of configuration with classical FILES backend

```
dhcpd__instances:
  4:
    mode: files
    listen_interfaces: wlan0
    subnets:
      - network: 192.168.1.0
        netmask: 255.255.255.0
        dhcp_options:
          subnet-mask: 255.255.255.0
          broadcast-address: 192.168.1.255
          routers: 192.168.1.254
        pools:
          - range: 192.168.1.100 192.168.1.190
            parameters:
              - allow unknown-clients
            dhcp_options:
              domain-name: home
              domain-name-servers: 192.168.1.254
            hosts:
              - name: tv_decoder
                mac_address: ee:ee:ee:ee:ee:ee
                deny: True
          - range: 192.168.1.80 192.168.1.99
            parameters:
              - deny unknown-clients
            groups:
              - dhcp_options:
                  domain-search: 'local'
                  domain-name: 'local'
                  domain-name-servers: 192.168.1.230
                hosts:
                  - name: laptop1
                    mac_address: ee:ee:ee:ee:ee:ee
```

  * Exemple of configuration with LDAP backend

```
dhcpd__instances:
  4:
    mode: files
    listen_interfaces: wlan0
    mode: ldap
    ldap_server: ldap.domain.net
    ldap_basedn: cn=dhcp,dc=example,dc=net
    ldap_debug_file: /tmp/dhcp-ldap-startup.log
```