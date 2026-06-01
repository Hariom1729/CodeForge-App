FROM gcc:latest

RUN useradd -m -s /bin/bash runner

WORKDIR /code

USER runner

# The command will be overridden by the execution manager
CMD ["/bin/bash"]
