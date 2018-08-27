FROM python:2.7

RUN apt-get update && \
    apt-get install -y \
        dvipng \
        latex-cjk-japanese \
        omake \
        python-sphinx \
        texlive-latex-extra && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -U \
        Sphinx==1.4.3 \
        sphinx_rtd_theme \
        sphinxcontrib-blockdiag \
        sphinxcontrib-rubydomain

ENTRYPOINT cd /data && omake clean html
