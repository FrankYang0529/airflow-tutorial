-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS "discord" (
    "id" SERIAL PRIMARY KEY,
    "content" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
DROP TABLE "discord";
-- +goose StatementEnd
