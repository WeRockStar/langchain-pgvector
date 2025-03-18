-- Add new schema named "public"
CREATE SCHEMA IF NOT EXISTS "public";
-- Set comment to schema: "public"
COMMENT ON SCHEMA "public" IS 'standard public schema';
-- Create "documents" table
CREATE TABLE "public"."documents" ("id" serial NOT NULL, "content" text NULL, "embedding" public.vector(1024) NULL, PRIMARY KEY ("id"));
