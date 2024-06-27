# Mocker DB

This class is a mock handler for simulating a vector database, designed primarily for testing and development scenarios.
It offers functionalities such as text embedding, hierarchical navigable small world (HNSW) search,
and basic data management within a simulated environment resembling a vector database.



```python
import sys
import numpy as np
sys.path.append('../')
from python_modules.mocker_db import MockerDB, SentenceTransformerEmbedder, MockerSimilaritySearch
```

## Usage examples

The examples contain:
1. Basic data insertion and retrieval
2. Text embedding and searching
3. Advanced filtering and removal
4. Testing the HNSW search algorithm
5. Simulating database connection and persistence


### 1. Basic Data Insertion and Retrieval


```python
# Initialization
handler = MockerDB(
    # optional
    embedder_params = {'model_name_or_path' : 'paraphrase-multilingual-mpnet-base-v2',
                        'processing_type' : 'batch',
                        'tbatch_size' : 500},
    embedder = SentenceTransformerEmbedder,
    ## optional/ for similarity search
    similarity_search_h = MockerSimilaritySearch,
    return_keys_list = [],
    search_results_n = 3,
    similarity_search_type = 'linear',
    similarity_params = {'space':'cosine'},
    ## optional/ inputs with defaults
    file_path = "./mock_persist",
    persist = True,
    embedder_error_tolerance = 0.0
)
# Initialize empty database
handler.establish_connection()

# Insert Data
values_list = [
    {"text": "Sample text 1"},
    {"text": "Sample text 2"}
]
handler.insert_values(values_list, "text")
print(f"Items in the database {len(handler.data)}")

# Retrieve Data
handler.filter_keys(subkey="text", subvalue="Sample text 1")
handler.search_database_keys(query='text')
results = handler.get_dict_results(return_keys_list=["text"])
print(results)

```


    .gitattributes:   0%|          | 0.00/744 [00:00<?, ?B/s]



    1_Pooling/config.json:   0%|          | 0.00/190 [00:00<?, ?B/s]



    README.md:   0%|          | 0.00/4.13k [00:00<?, ?B/s]



    config.json:   0%|          | 0.00/723 [00:00<?, ?B/s]



    config_sentence_transformers.json:   0%|          | 0.00/122 [00:00<?, ?B/s]



    model.safetensors:   0%|          | 0.00/1.11G [00:00<?, ?B/s]



    pytorch_model.bin:   0%|          | 0.00/1.11G [00:00<?, ?B/s]



    sentence_bert_config.json:   0%|          | 0.00/53.0 [00:00<?, ?B/s]



    sentencepiece.bpe.model:   0%|          | 0.00/5.07M [00:00<?, ?B/s]



    special_tokens_map.json:   0%|          | 0.00/239 [00:00<?, ?B/s]



    tokenizer.json:   0%|          | 0.00/9.08M [00:00<?, ?B/s]



    tokenizer_config.json:   0%|          | 0.00/402 [00:00<?, ?B/s]



    modules.json:   0%|          | 0.00/229 [00:00<?, ?B/s]


    Items in the database 2
    [{'text': 'Sample text 1'}]


### 2. Text Embedding and Searching


```python
ste = SentenceTransformerEmbedder(# optional / adaptor parameters
                                  processing_type = '',
                                  tbatch_size = 500,
                                  max_workers = 2,
                                  # sentence transformer parameters
                                  model_name_or_path = 'paraphrase-multilingual-mpnet-base-v2',)
```


```python
# Single Text Embedding
query = "Sample query"
embedded_query = ste.embed(query,
                           # optional
                           processing_type='')
print(embedded_query[0:50])
```

    [-0.04973586  0.09520268 -0.01219508  0.09253863 -0.02301829 -0.02721018
      0.0568395   0.09710983  0.10683874  0.05812277  0.1322755   0.01142832
     -0.06957253  0.0698075  -0.05259365 -0.05755996  0.00816183 -0.0083684
     -0.00861256  0.01442069  0.01188816 -0.09503672  0.07125735 -0.04827785
      0.01473162  0.01084185 -0.1048248   0.07012521 -0.04720647  0.10030048
      0.04455933  0.02131893  0.00667914 -0.05259187  0.06822995 -0.09520472
     -0.00581363 -0.02451877 -0.00384987  0.02750723  0.06960277  0.2401375
     -0.01220019  0.05890937 -0.08468664  0.11379692 -0.03594767 -0.0565297
     -0.01621809  0.09546725]



```python
# Batch Text Embedding
queries = ["Sample query", "Sample query 2"]
embedded_query = ste.embed(queries,
                           # optional
                           processing_type='batch')
print(embedded_query[0][0:50])
print("---")
print(embedded_query[1][0:50])
```

    [-0.04973584  0.09520271 -0.01219508  0.09253865 -0.0230183  -0.02721017
      0.05683954  0.09710982  0.10683876  0.05812274  0.13227552  0.01142829
     -0.06957256  0.06980743 -0.05259361 -0.05755996  0.00816183 -0.00836839
     -0.00861252  0.01442068  0.01188819 -0.09503672  0.07125732 -0.04827787
      0.01473164  0.01084186 -0.1048249   0.07012525 -0.04720649  0.10030047
      0.04455935  0.02131895  0.00667912 -0.05259192  0.06822995 -0.09520471
     -0.00581363 -0.02451887 -0.00384988  0.02750726  0.06960279  0.2401375
     -0.01220022  0.05890937 -0.08468666  0.11379688 -0.03594765 -0.05652964
     -0.0162181   0.09546735]
    ---
    [-0.05087024  0.1231768  -0.0139253   0.10524713 -0.07614321 -0.02349629
      0.05829773  0.15128359  0.18119803  0.03745934  0.12174664  0.00639838
     -0.04045055  0.12758303 -0.06155453 -0.06736137  0.04713943 -0.04134275
     -0.12165949  0.0440988   0.01834145 -0.04796624  0.04922185 -0.00641203
      0.01420631 -0.03602944 -0.01026761  0.09232258 -0.04927172  0.03985452
      0.03566906  0.0833893   0.04922603 -0.09951889  0.0513812  -0.13344644
      0.01626778 -0.01189724  0.0059921   0.05663403  0.04282105  0.26432782
     -0.01122811  0.07177631 -0.11822144  0.08731946 -0.04965353  0.03697515
      0.08965266  0.03107021]



```python
# Search Database
search_results = handler.search_database(query, return_keys_list=["text"])

# Display Results
print(search_results)

```

    [{'text': 'Sample text 1'}]


### 3. Advanced Filtering and Removal


```python
# Advanced Filtering
filter_criteria = {"text": "Sample text 1"}
handler.filter_database(filter_criteria)
filtered_data = handler.filtered_data
print(f"Filtered data {len(filtered_data)}")

# Data Removal
handler.remove_from_database(filter_criteria)
print(f"Items left in the database {len(handler.data)}")

```

    Filtered data 1
    Items left in the database 1


### 4. Testing the HNSW Search Algorithm


```python
mss = MockerSimilaritySearch(
    # optional
    search_results_n = 3,
    similarity_params = {'space':'cosine'},
    similarity_search_type ='linear'
)
```


```python
# Create embeddings
embeddings = [ste.embed("example1"), ste.embed("example2")]


# Assuming embeddings are pre-calculated and stored in 'embeddings'
data_with_embeddings = {"record1": {"embedding": embeddings[0]}, "record2": {"embedding": embeddings[1]}}
handler.data = data_with_embeddings

# HNSW Search
query_embedding = embeddings[0]  # Example query embedding
labels, distances = mss.hnsw_search(query_embedding, np.array(embeddings), k=1)
print(labels, distances)

```

    [0] [4.172325e-07]


### 5. Simulating Database Connection and Persistence


```python
# Establish Connection
handler.establish_connection()

# Change and Persist Data
handler.insert_values([{"text": "New sample text"}], "text")
handler.save_data()

# Reload Data
handler.establish_connection()
print(f"Items in the database {len(handler.data)}")

```

    Items in the database 2

