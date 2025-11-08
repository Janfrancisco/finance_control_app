#+++++++++++++++++++++++++++++++++++
#    First step: Build
#+++++++++++++++++++++++++++++++++++

FROM python:3.12-slim AS builder

ARG ENVIRONMENT=prod

WORKDIR /financial

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema necessárias para  o pacotes Python e o WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libgdk-pixbuf-2.0-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*


COPY requirements /tmp/requirements 

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps -r /tmp/requirements/${ENVIRONMENT}.txt -w /wheels

# RUN pip install --no-cache-dir -r /tmp/requirements/${ENVIRONMENT}.txt

#+++++++++++++++++++++++++++++++++++
#    2nd step: Runtime
#+++++++++++++++++++++++++++++++++++

FROM python:3.12-slim

ARG ENVIRONMENT=prod
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    ENVIRONMENT=${ENVIRONMENT}


RUN echo "---------------------------------------"
RUN echo "Valor do argumento AMBIENTE_BUILD: ${ENVIRONMENT}"
RUN echo "---------------------------------------"

WORKDIR /financial

# Instala apenas as libs necessárias em tempo de execução (sem build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copia as dependências Python já compiladas da etapa builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

RUN echo "---------------------------------------"
RUN echo "Valor do argumento AMBIENTE_BUILD: ${ENVIRONMENT}"
RUN echo "---------------------------------------"

# Copia o entrypoint
COPY entrypoint.sh /app/
# Corrige quebras de linha CRLF -> LF para evitar erro "no such file or directory" em sistemas Linux
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Define variável de ambiente padrão
# ENV ENVIRONMENT=dev

# Usa o entrypoint para decidir o comando final
ENTRYPOINT ["/app/entrypoint.sh"]