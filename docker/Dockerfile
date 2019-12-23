#
# Fedora / M2Siame / TP docker
#

FROM fedora:latest AS sam

# Location of files to add to the container
# Note this <relative_path> to the build env @ host
ENV DOCKYARD dockyard

# Switch to root user to enable installation (default)
USER root

# Copy configuration directory
COPY ${DOCKYARD} /${DOCKYARD}

# Various packages to install and final update
# passwd was generated using 'openssl passwd -1'
RUN echo 'root:root' | chpasswd -e \
    && cp -af /${DOCKYARD}/root / \
    && mkdir -p /root/.ssh \
    && cp -af /${DOCKYARD}/authorized_keys /root/.ssh/ \
    && chmod 600 /root/.ssh/authorized_keys \
    && chmod g-w /root \
    && dnf -y remove vim-minimal \
    && dnf -y install \
    procps \
    tmux \
    vim \
    openssh-server \
    openssh-clients \
    supervisor \
    python3-pip \
    python3-psycopg2 \
    uwsgi \
    uwsgi-plugin-python3 \
    redis \
    && dnf -y --nogpgcheck --allowerasing upgrade \
    && dnf clean all \
    && cp -af /${DOCKYARD}/supervisord.d /etc \
    && mkdir -p /var/run/sshd \
    && ssh-keygen -A \
    && pip3 install -r /${DOCKYARD}/requirements.txt

# Ports for sshd and django application
EXPOSE 22 2220

# ENTRYPOINT
CMD [ "/usr/bin/supervisord", "-n" ]