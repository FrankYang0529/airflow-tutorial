-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS "result" (
    "id" SERIAL PRIMARY KEY,
    "content_id" integer NOT NULL,
    "content" VARCHAR(255) NOT NULL,
    "content_timestamp" TIMESTAMPTZ NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
DROP TABLE "result";
-- +goose StatementEnd
