FROM python:3.10

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY /src .

RUN mkdir -p /root/.streamlit

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > /root/.streamlit/config.toml'

EXPOSE 8501
ENV PORT=8501

CMD streamlit run app.py --server.port $PORT --server.headless true --server.fileWatcherType none --browser.gatherUsageStats false