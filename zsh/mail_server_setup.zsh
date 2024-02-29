#!/bin/zsh

# Script to set up and configure a Postfix mail server with Dovecot

# Ensure the script is running as root
if (( $EUID != 0 )); then
  echo "Please run as root"
  exit
fi

# Install postfix, dovecot, and mailutils
apt-get update && apt-get install -y postfix dovecot-core dovecot-imapd mailutils

# Postfix configuration
postfix_config() {
  postconf -e 'smtpd_banner = $myhostname ESMTP $mail_name'
  postconf -e 'biff = no'
  postconf -e 'append_dot_mydomain = no'
  postconf -e 'readme_directory = no'
  postconf -e 'smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem'
  postconf -e 'smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key'
  postconf -e 'smtpd_use_tls=yes'
  postconf -e 'smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache'
  postconf -e 'smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache'
  postconf -e 'myhostname = example.com'
  postconf -e 'alias_maps = hash:/etc/aliases'
  postconf -e 'myorigin = /etc/mailname'
  postconf -e 'mydestination = $myhostname, localhost.$mydomain, $mydomain'
  postconf -e 'relayhost ='
  postconf -e 'mynetworks = 127.0.0.0/8[::1]/128'
  postconf -e 'mailbox_size_limit = 0'
  postconf -e 'recipient_delimiter = +'
  postconf -e 'inet_interfaces = all'
  postconf -e 'inet_protocols = all'
  
  # Set up aliases
  echo "root: user@example.com" >> /etc/aliases
  newaliases
}

# Dovecot configuration
dovecot_config() {
  # Enable IMAP
  sed -i 's/#protocols = imap pop3 lmtp/protocols = imap lmtp/' /etc/dovecot/dovecot.conf
  
  # Mailbox settings
  sed -i 's/#mail_location = /mail_location = maildir:~\/Maildir/' /etc/dovecot/conf.d/10-mail.conf
  
  # Enable SSL
  sed -i 's/#ssl = yes/ssl = yes/' /etc/dovecot/conf.d/10-ssl.conf
  sed -i "s#ssl_cert = </etc/dovecot/private/dovecot.pem#ssl_cert = </etc/ssl/certs/ssl-cert-snakeoil.pem#" /etc/dovecot/conf.d/10-ssl.conf
  sed -i "s#ssl_key = </etc/dovecot/private/dovecot.key#ssl_key = </etc/ssl/private/ssl-cert-snakeoil.key#" /etc/dovecot/conf.d/10-ssl.conf
}

# Configure Postfix and Dovecot
postfix_config
dovecot_config

# Restart services
systemctl restart postfix
systemctl restart dovecot

echo "Mail server setup complete."
