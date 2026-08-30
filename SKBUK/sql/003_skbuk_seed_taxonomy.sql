insert into public.tod_taxonomy (code, name, taxonomy_type) values
('B01','Organisation identity','bidder'),('B02','Bidding structure','bidder'),('B03','Exclusion declarations','bidder'),('B04','Financial standing','bidder'),('B05','Insurance','bidder'),('B06','Mandatory policies','bidder'),('B07','Certificates','bidder'),('B08','Delivery capability','bidder'),('B09','Tender responses','bidder'),('B10','Submission evidence','bidder'),
('MOUUK-0001','Procurement Act 2023','official'),('MOUUK-0002','Procurement Regulations 2024','official'),('MOUUK-0026','Evidence and Provenance','official')
on conflict (code) do nothing;
