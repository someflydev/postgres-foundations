\connect pgfound

DO $$
BEGIN
  RAISE NOTICE 'pgfound lab booted on host %, PostgreSQL %, at %',
    inet_server_addr(),
    version(),
    clock_timestamp();
END
$$;
