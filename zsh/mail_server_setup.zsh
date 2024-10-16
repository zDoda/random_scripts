#!/bin/zsh

# Check if the script is being run as root
if (( $EUID != 0 )); then
    echo "Please run as root"
    exit
fi

# Update the system
apt-get update && apt-get upgrade -y

# Install mail server packages
apt-get install postfix dovecot-core dovecot-imapd mailutils -y

# Configure Postfix
postconf -e 'smtpd_banner = $myhostname ESMTP $mail_name'
postconf -e 'biff = no'
postconf -e 'append_dot_mydomain = no'
postconf -e 'readme_directory = no'
postconf -e 'myhostname = example.com'
postconf -e 'myorigin = /etc/mailname'
postconf -e 'mydestination = $myhostname, example.com, localhost.com, , localhost'
postconf -e 'relayhost = '
postconf -e 'mynetworks = 127.0.0.0/8'
postconf -e 'mailbox_size_limit = 0'
postconf -e 'recipient_delimiter = +'
postconf -e 'inet_interfaces = all'
postconf -e 'inet_protocols = all'

# Set up mailboxes to use Maildir instead of mbox
postconf -e "home_mailbox = Maildir/"

# Secure Postfix with TLS
postconf -e "smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem"
postconf -e "smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key"
postconf -e "smtpd_use_tls=yes"
postconf -e "smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache"
postconf -e "smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache"

# Restart and enable Postfix service
systemctl restart postfix
systemctl enable postfix

# Configure Dovecot
# Set up IMAP and enable SSL
[[ -f /etc/dovecot/conf.d/10-mail.conf ]] && \
sed -i 's|^mail_location = .*|mail_location = maildir:~/Maildir|' /etc/dovecot/conf.d/10-mail.conf

[[ -f /etc/dovecot/conf.d/10-auth.conf ]] && \
sed -i 's|^disable_plaintext_auth = .*|disable_plaintext_auth = no|' /etc/dovecot/conf.d/10-auth.conf

[[ -f /etc/dovecot/conf.d/10-ssl.conf ]] && \
sed -i 's|^ssl = .*|ssl = yes|' /etc/dovecot/conf.d/10-ssl.conf \
    && sed -i 's|^ssl_cert = <.*|ssl_cert = </etc/ssl/certs/dovecot.pem|' /etc/dovecot/conf.d/10-ssl.conf \
    && sed -i 's|^ssl_key = <.*|ssl_key = </etc/ssl/private/dovecot.pem|' /etc/dovecot/conf.d/10-ssl.conf

# Add user vmail
groupadd -g 5000 vmail
useradd -g vmail -u 5000 vmail -d /var/mail

# Restart and enable Dovecot service
systemctl restart dovecot
systemctl enable dovecot

echo "Mail server setup is complete."
