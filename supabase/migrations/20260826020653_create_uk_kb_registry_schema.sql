create type public.document_family as enum ('primary-legislation','secondary-legislation','explanatory-notes','guidance','policy-notes','supplier-guidance','training-manual','consultation','misc');
create type public.document_status as enum ('active','superseded','missing','rejected');
create type public.run_status as enum ('completed','running','failed','partial');
create type public.rejection_reason as enum ('robots_unreadable','robots_disallowed','host_not_allowlisted','not_pdf','http_error','invalid_content_type','duplicate_hash','fetch_failed','classification_failed','path_policy_blocked');

create table public.sources (
	source_id text primary key check (source_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]*$'),
	source_name text not null check (char_length(source_name) between 3 and 300),
	landing_url text not null check (landing_url ~ '^https?://'),
	publisher text not null check (publisher in ('gov.uk','legislation.gov.uk')),
	jurisdiction text default 'UK',
	category_hint public.document_family,
	enabled boolean not null default true,
	robots_status text not null default 'unknown' check (robots_status in ('allowed','disallowed','unreadable','unknown')),
	last_robots_checked_at timestamptz,
	notes text,
	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now()
);

create table public.runs (
	run_id text primary key check (run_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]*$'),
	started_at timestamptz not null,
	finished_at timestamptz,
	status public.run_status not null,
	app_version text not null,
	source_count integer not null check (source_count >= 0),
	discovered_count integer not null check (discovered_count >= 0),
	downloaded_count integer not null check (downloaded_count >= 0),
	unchanged_count integer not null check (unchanged_count >= 0),
	rejected_count integer not null check (rejected_count >= 0),
	error_count integer not null check (error_count >= 0),
	report_path text,
	log_path text,
	created_at timestamptz not null default now(),
	check (finished_at is null or finished_at >= started_at)
);

create table public.documents (
	document_id text primary key check (document_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]*$'),
	canonical_slug text not null check (canonical_slug ~ '^[a-z0-9]+(?:-[a-z0-9]+)*$'),
	title text not null check (char_length(title) between 3 and 600),
	publisher text not null check (publisher in ('gov.uk','legislation.gov.uk')),
	source_id text not null references public.sources(source_id),
	document_family public.document_family not null,
	document_type text not null default 'pdf' check (document_type = 'pdf'),
	jurisdiction text default 'UK',
	applicability text default 'public-procurement',
	year integer check (year between 1200 and 2200),
	language text not null default 'en',
	authoritative_url text not null check (authoritative_url ~ '^https?://'),
	landing_url text not null check (landing_url ~ '^https?://'),
	canonical_page_url text check (canonical_page_url is null or canonical_page_url ~ '^https?://'),
	first_seen_at timestamptz not null,
	first_seen_run_id text not null references public.runs(run_id),
	latest_seen_at timestamptz not null,
	latest_seen_run_id text not null references public.runs(run_id),
	latest_version_id text,
	latest_sha256 text check (latest_sha256 is null or latest_sha256 ~ '^[a-f0-9]{64}$'),
	latest_download_url text check (latest_download_url is null or latest_download_url ~ '^https?://'),
	latest_http_status integer check (latest_http_status between 200 and 599),
	latest_content_type text check (latest_content_type is null or lower(split_part(latest_content_type, ';', 1)) = 'application/pdf'),
	latest_content_length bigint check (latest_content_length is null or latest_content_length > 0),
	latest_etag text,
	latest_last_modified text,
	latest_downloaded_at timestamptz,
	latest_file_name_original text,
	latest_file_path_current text,
	latest_file_path_versioned text,
	version_count integer not null default 0 check (version_count >= 0),
	status public.document_status not null default 'active',
	supersedes_document_id text references public.documents(document_id),
	notes text,
	created_at timestamptz not null default now(),
	updated_at timestamptz not null default now(),
	check (latest_seen_at >= first_seen_at),
	check (latest_file_path_current is null or latest_file_path_current like 'data/documents/%'),
	check (latest_file_path_versioned is null or latest_file_path_versioned like 'data/documents/%')
);

create table public.document_versions (
	version_id text primary key check (version_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]*$'),
	document_id text not null references public.documents(document_id) on delete cascade,
	run_id text not null references public.runs(run_id),
	download_url text not null check (download_url ~ '^https?://'),
	http_status integer not null check (http_status between 200 and 599),
	content_type text not null check (lower(split_part(content_type, ';', 1)) = 'application/pdf'),
	content_length bigint check (content_length is null or content_length > 0),
	etag text,
	last_modified text,
	sha256 text not null check (sha256 ~ '^[a-f0-9]{64}$'),
	file_name_original text,
	file_path_current text not null check (file_path_current like 'data/documents/%'),
	file_path_versioned text not null check (file_path_versioned like 'data/documents/%'),
	discovered_at timestamptz not null,
	downloaded_at timestamptz not null,
	is_binary_changed boolean not null,
	change_reason text,
	version_label text,
	created_at timestamptz not null default now(),
	unique (document_id, sha256)
);

alter table public.documents add constraint documents_latest_version_fk foreign key (latest_version_id) references public.document_versions(version_id) deferrable initially deferred;

create table public.rejections (
	rejection_id text primary key check (rejection_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]*$'),
	run_id text not null references public.runs(run_id) on delete cascade,
	source_id text references public.sources(source_id),
	url text not null check (url ~ '^https?://'),
	landing_url text check (landing_url is null or landing_url ~ '^https?://'),
	host text not null,
	reason_code public.rejection_reason not null,
	detail text,
	robots_status text check (robots_status is null or robots_status in ('allowed','disallowed','unreadable','unknown')),
	occurred_at timestamptz not null
);

create index documents_source_id_idx on public.documents(source_id);
create index documents_status_idx on public.documents(status);
create index documents_latest_sha256_idx on public.documents(latest_sha256);
create index document_versions_document_id_idx on public.document_versions(document_id);
create index document_versions_sha256_idx on public.document_versions(sha256);
create index rejections_run_id_idx on public.rejections(run_id);
create index rejections_reason_code_idx on public.rejections(reason_code);

alter table public.sources enable row level security;
alter table public.runs enable row level security;
alter table public.documents enable row level security;
alter table public.document_versions enable row level security;
alter table public.rejections enable row level security;

revoke all on public.sources, public.runs, public.documents, public.document_versions, public.rejections from anon, authenticated;
grant all on public.sources, public.runs, public.documents, public.document_versions, public.rejections to service_role;
