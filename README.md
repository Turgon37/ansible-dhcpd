Ansible Role DHCP Daemon
========

:warning: This role is under development

This roles configure an dhcp server

## OS Family

This role is available for Debian and CentOS

## Features

At this day the role can be used to configure :

  * Install dhcpd
  * Configure dhcpd in mode FILE with subnets and hosts declarations
  * Configure dhcpd in mode LDAP

## Configuration

The variables that can be passed to this role and a brief description about them are as follows:

| Name              | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| dhcpd__mode       | Choose dhcpd mode in 'files' or 'ldap'. (See below for mode specific options)|
| dhcpd__interfaces | The name of the interfaces on which dhcpd will listen (default all)          |


### Mode FILES

| Name                 | Description                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| dhcpd__authoritative | Boolean that make this DHCP server authoritative (not a relay)                                                                                |
| dhcpd__dhcp_options  | Global DHCP option that applies on all subnet. !! Take care that some option require double quote, see example below with 'domain-name' option|
| dhcpd__dhcp_subnets  |                                                                                                                                               |
| dhcpd__dhcp_hosts    |                                                                                                                                               |


### Mode LDAP

| Name                   | Description                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------- |
| dhcpd__ldap_server     | The ip address/domain name of the LDAP server                                                        |
| dhcpd__ldap_port       | The port to use to bind with LDAP server                                                             |
| dhcpd__ldap_username   | OPTIONAL bind username/dn                                                                            |
| dhcpd__ldap_password   | OPTIONAL bind password                                                                               |
| dhcpd__ldap_basedn     | LDAP base DN of the DHCP tree                                                                        |
| dhcpd__ldap_servercn   | The commonname (cn= field) of the DhcpServer entry to use. (default is to use the fqdn of this host) |
| dhcpd__ldap_method     | The LDAP query method, 'static' or 'dynamic'                                                         |
| dhcpd__ldap_debug_file | OPTIONAL The debug file in which dhcpd will dump read LDAP configuration                             |



### Example

  * Exemple of configuration with classical FILES backend

```
dhcpd__mode: files
dhcpd__dhcp_options:
  domain-name: '"domain.example.net"'
  domain-name-servers: 192.168.1.254
dhcpd__interfaces: 'wlan0'
dhcpd__dhcp_subnets:
  - address: 192.168.1.0
    netmask: 255.255.255.0
    range: 192.168.1.10 192.168.1.100
    dhcp_options:
      routers: 192.168.1.254
      broadcast-address: 192.168.1.255
dhcpd__dhcp_hosts:
  host_name1:
    hardware_ethernet: aa:aa:aa:aa:aa:aa
    fixed_address: 192.168.1.101
  host_name2:
    hardware_ethernet: aa:aa:aa:aa:aa:aa
    fixed_address: 192.168.1.102
```

  * Exemple of configuration with LDAP backend

```
dhcpd__mode: ldap
dhcpd__ldap_server: ldap.domain.net
dhcpd__ldap_basedn: cn=dhcp,dc=example,dc=net
dhcpd__ldap_debug_file: /tmp/dhcp-ldap-startup.log
```