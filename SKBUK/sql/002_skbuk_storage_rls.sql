insert into storage.buckets (id, name, public) values ('tod-official','tod-official',false), ('tod-bidder','tod-bidder',false), ('tod-tenders','tod-tenders',false), ('tod-exports','tod-exports',false) on conflict (id) do update set public = false;
revoke all on table public.tod_taxonomy, public.tod_organisations, public.tod_tenders, public.tod_source_documents, public.tod_document_versions, public.tod_source_excerpts, public.tod_inspection_runs, public.tod_inspection_sources, public.tod_compliance_checks, public.tod_ingestion_runs, public.tod_ingestion_events, public.tod_document_module_routes from anon, authenticated;
alter table public.tod_taxonomy enable row level security;
alter table public.tod_organisations enable row level security;
alter table public.tod_tenders enable row level security;
alter table public.tod_source_documents enable row level security;
alter table public.tod_document_versions enable row level security;
alter table public.tod_source_excerpts enable row level security;
alter table public.tod_inspection_runs enable row level security;
alter table public.tod_inspection_sources enable row level security;
alter table public.tod_compliance_checks enable row level security;
alter table public.tod_ingestion_runs enable row level security;
alter table public.tod_ingestion_events enable row level security;
alter table public.tod_document_module_routes enable row level security;
-- No storage policies are created: anonymous/browser access is denied by default.
