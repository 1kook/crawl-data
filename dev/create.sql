CREATE TABLE 'btc_price' (
    open_time TIMESTAMPTZ NOT NULL,
    open_price DOUBLE PRECISION NOT NULL,
    high_price DOUBLE PRECISION NOT NULL,
    low_price DOUBLE PRECISION NOT NULL,
    close_price DOUBLE PRECISION NOT NULL,
    volume DOUBLE PRECISION NOT NULL,
    close_time TIMESTAMPTZ NOT NULL,
    quote_asset_volume DOUBLE PRECISION NOT NULL,
)