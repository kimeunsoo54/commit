!pip install yt-dlp
!pip install git+https://github.com/openai/whisper.git -q 

import whisper
import warnings
warnings.filterwarnings('ignore')


!yt-dlp -f 'ba' -x --audio-format mp3 https://youtu.be/kfl7ufDvCGw?si=Y35pu6xsbIgvM3m6  -o 'tmp'
model = whisper.load_model("small")
transcription = model.transcribe('/content/tmp.mp3')
res = transcription['segments']


from datetime import datetime

def store_segments(segments):
  texts = []
  start_times = []

  for segment in segments:
    text = segment['text']
    start = segment['start']

    # Convert the starting time to a datetime object
    start_datetime = datetime.fromtimestamp(start)

    # Format the starting time as a string in the format "00:00:00"
    formatted_start_time = start_datetime.strftime('%H:%M:%S')

    texts.append("".join(text))
    start_times.append(formatted_start_time)

  return texts, start_times

texts, start_times = store_segments(res)

file_name = "test.txt"
with open(file_name, 'w+') as file:
  file.write('\n'.join(texts))



%%capture
!pip install langchain
!pip install openai
!pip install faiss-cpu



from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain import OpenAI
import openai
import faiss


import os
os.environ["OPENAI_API_KEY"] = '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'


text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = []
metadatas = []
for i, d in enumerate(texts):
    splits = text_splitter.split_text(d)
    docs.extend(splits)
    metadatas.extend([{"source": start_times[i]}] * len(splits))
embeddings = OpenAIEmbeddings()




store = FAISS.from_texts(docs, embeddings, metadatas=metadatas)
faiss.write_index(store.index, "docs.index")


from langchain.docstore.document import Document
summaryDoc = [Document(page_content=t) for t in texts[:3]]
