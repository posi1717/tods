create extension if not exists pg_cron with schema pg_catalog;
create extension if not exists pg_net;

select cron.unschedule('uk-kb-collector-hourly')
where exists (
  select 1 from cron.job where jobname = 'uk-kb-collector-hourly'
);

select cron.schedule(
  'uk-kb-collector-hourly',
  '0 * * * *',
  $$
  select case
    when exists (
      select 1
      from vault.decrypted_secrets
      where name = 'ukkb-os'
    ) then net.http_post(
      url := 'https://api.github.com/repos/Donny1717/UKKB/actions/workflows/collect-pdfs.yml/dispatches',
      headers := jsonb_build_object(
        'Accept', 'application/vnd.github+json',
        'Authorization', 'Bearer ' || (
          select decrypted_secret
          from vault.decrypted_secrets
          where name = 'ukkb-os'
        ),
        'X-GitHub-Api-Version', '2022-11-28',
        'Content-Type', 'application/json'
      ),
      body := '{"ref":"main"}'::jsonb
    )
    else null
  end;
  $$
);