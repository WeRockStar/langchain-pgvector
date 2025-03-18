table "documents" {
  schema = schema.public
  column "id" {
    null = false
    type = serial
  }
  column "content" {
    null = true
    type = text
  }
  column "embedding" {
    null = true
    type = sql("public.vector(1024)")
  }
  primary_key {
    columns = [column.id]
  }
}
schema "public" {
  comment = "standard public schema"
}
