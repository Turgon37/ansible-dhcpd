Ansible Role DHCP Daemon
=========

[![Build Status](https://travis-ci.org/Turgon37/ansible-dhcpd.svg?branch=master)](https://travis-ci.org/Turgon37/ansible-dhcpd)

:warning: This role is under development, some important (and possibly breaking) changes may happend. Don't use it in production level environments but you can eventually base your own role on this one :hammer:

:grey_exclamation: Before using this role, please know that all my Ansible roles are fully written and accustomed to my IT infrastructure. So, even if they are as generic as possible they will not necessarily fill your needs, I advice you to carrefully analyse what they do and evaluate their capability to be installed securely on your servers.

**This roles configure the isc-dhcp-server to use files or LDAP backend.**

## Features

Currently this role provide the following features :

  * dhcpd installation
  * dhcpd configuration in plain text FILEs with
    * subnets
    * hosts
    * groups
    * pools
    * options declarations
    * OMAPI configuration
    * secret keys (with automatic secret generation available)
  * dhcpd configuration in mode LDAP
  * [local facts](#facts)

## Requirements

### OS Family

This role is available for Debian and RedHat/CentOS

### Dependencies

--


## Role Variables

The variables that can be passed to this role and a brief description about them are as follows:

| Name                   | Types/Values   | Description                                                                                |
| -----------------------| ---------------|------------------------------------------------------------------------------------------- |
| dhcpd__facts           | Boolean        | Install the local fact script                                                              |
| dhcpd__service_enabled | Boolean        | Enable or not the service                                                                  |
| dhcpd__mode            | String         | Choose dhcpd configuration mode in 'files' or 'ldap'. (See below for mode specific options)|
| dhcpd__interfaces      | List of String | List of interface on which dhcpd will listen for DHCP requests (default all)               |

### Mode FILES

| Name                       | Types/Values             | Description                                                   |
| ---------------------------| -------------------------|-------------------------------------------------------------- |
| dhcpd__authoritative       | Boolean                  | Boolean that make this DHCP server authoritative (not a relay)|
| dhcpd__parameters          | List of String           | Dhcp parameters in raw string format to apply on configuraton |
| dhcpd__dhcp_options        | Dict of String           | Dhcp option in "key: value" format                            |
| dhcpd__subnets             | List of Subnet statements| Declare subnets                                               |
| dhcpd__hosts               | List of Host statements  | Hosts entries at the root of the configuration                |
| dhcpd__keys                | List of key statements   | List of secret keys to configure (see below )                 |
| dhcpd__omapi_enabled       | Boolean                  | Enable (open) or not the OMAPI                                |
| dhcpd__omapi_port          | Integer                  | Port of OMAPI interface                                       |

Note for *dhcp_options*, some parameters need to be enclosed by quote in the configuration file, this role takes with a list of theses options (dhcpd__quoted_dhcp_options_name) and apply automatically the quotes. So, normally you do not have to put theses quotes in inventory files.

#### Key statements

Ansible manage the list of secret keys declared for DHCPD. Each key item must be set in the dhcpd__keys dict, see below two examples:

```
dhcpd__keys:
  key1:
    algorithm: hmac-sha1
    secret: XXXXXXXX==
  ddns:
    algorithm: hmac-md5
    # secret will be autogenerate
```

If you do not provide the 'secret' key, it will be auto generated (only at first Ansible application) according the selected algorithm.
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

| Name                   | Types/Values | Description                                                                                           |
| ---------------------- | -------------|-------------------------------------------------------------------------------------------------------|
| dhcpd__ldap_server     | String       | The ip address/domain name of the LDAP server                                                         |
| dhcpd__ldap_port       | Integer      | The port to use to bind with LDAP server                                                              |
| dhcpd__ldap_username   | String       | OPTIONAL bind username/dn                                                                             |
| dhcpd__ldap_password   | String       | OPTIONAL bind password                                                                                |
| dhcpd__ldap_basedn     | String       | LDAP base DN of the DHCP tree                                                                         |
| dhcpd__ldap_servercn   | String       | The commonname (cn= field) of the DhcpServer entry to use. (default is to use the fqdn of this host)  |
| dhcpd__ldap_method     | String       | The LDAP query method, 'static' or 'dynamic'                                                          |
| dhcpd__ldap_debug_file | String       | OPTIONAL The debug file in which dhcpd will dump read LDAP configuration                              |


## Facts

By default the local fact are installed and expose the following variables :


* ```ansible_local.dhcpd.version_full```
* ```ansible_local.dhcpd.version_major```


## Examples Playbooks

To use this role create or update your playbook according the following examples :

  * Exemple of configuration with classical FILES backend

```
    - hosts: servers
      roles:
         - dhcpd
      vars:
        dhcpd__mode: files
        dhcpd__interfaces: 'wlan0'
        dhcpd__parameters:
          - default-lease-time 864000
          - deny bootp
          - ddns-updates off
          - ddns-update-style none
          - log-facility local7
        dhcpd__subnets:
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
    - hosts: servers
      roles:
         - dhcpd
      vars:
        dhcpd__subnets:
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

    - hosts: servers
      roles:
         - dhcpd
      vars:
        dhcpd__mode: ldap
        dhcpd__ldap_server: ldap.domain.net
        dhcpd__ldap_basedn: cn=dhcp,dc=example,dc=net
        dhcpd__ldap_debug_file: /tmp/dhcp-ldap-startup.log
```


## License

MIT