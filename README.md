# Learning How to Work with pgvector

## Introduction

This is a playground for me to learn how to work with `pgvector`.

## pgvector

- Enable the extension:
	```sql
	CREATE EXTENSION IF NOT EXISTS vector;
	```
- Create `documents` table and we will use `embedding` column as a vector of 1024 dimensions:
	```sql
	CREATE TABLE IF NOT EXISTS documents (id SERIAL PRIMARY KEY, content TEXT, embedding vector(1024));
	```
	Note: Dimension of the vector can be changed as per the requirement of precision we need.
