USE mrds_v1;
SET FOREIGN_KEY_CHECKS=0;
#truncate user;

truncate user_type;
INSERT INTO user_type
(
user_type_id,
user_type,
is_active)
VALUES
('1', 'Patient', true),
('2', 'PT', true),
('3', 'DR', true),
('4', 'Admin', true);

truncate specialization;
INSERT INTO specialization
(
specialization,
keywords,
user_type_id,
is_active)
VALUES
('Orthopaedic','Orthopaedic', 2, true),
('Sports','Sports', 2, true),
('Rehabilitation','Rehabilitation', 2, true),
('Post fracture stiffness','Post fracture stiffness', 2, true),
('Joint pain','Joint pain', 2, true),
('Gout','Gout', 2, true),
('Tennis elbow','Tennis elbow',2 , true),
('Stroke CVA','Stroke CVA',3 , true),
('Neuro','Neuro', 3, true),
('Nerve root  compression','Nerve root  compression', 3, true),
('Spinal cord injury','Spinal cord injury', 3, true),
('Multiple sclerosis','Multiple sclerosis',3 , true),
('Sciatica','Sciatica', 3, true),
('Delayed milestones with Motor control','Delayed milestones with Motor control', 3, true),
('Ataxia','Ataxia',3 , true),
('Antonia','Antonia',3 , true);


truncate qualification;
INSERT INTO qualification
(
qualification,
keywords,
user_type_id,
is_active)
VALUES
('BPT','BPT',2, true),
('MPT','MPT',2, true),
('MBBS','MBBS',3, true),
('D Ortho','D Ortho',3, true),
('MD','MD',3, true);

truncate subscription;
INSERT INTO subscription
(
subscription_name,
subscription_details,
subscription_validity,
cost,
is_active,
user_type_id)
VALUES
('One-Month','1 Month',1, 100, true, 1),
('Six-Month','6 Month',6, 500, true, 1),
('One-Year','1 Year',12, 800, true, 1),
('One-Month','1 Month',1, 200, true, 2),
('Six-Month','6 Month',6, 1000, true, 2),
('One-Year','1 Year',12, 1600, true, 2),
('One-Month','1 Month',1, 300, true, 3),
('Six-Month','6 Month',6, 1500, true, 3),
('One-Year','1 Year',12, 2500, true, 3);



truncate package;
INSERT INTO package
(
package_name,
details,
cost,
is_active)
VALUES
('Spinal pain (neck/back) without nerve compression ','Spinal pain (neck/back) without nerve compression ',1, true),
('Spinal pain (neck/back) with nerve compression ','Spinal pain (neck/back) with nerve compression ',1.25, true),
('Needle Therapy','Needle Therapy',2, true),
('Cupping  Therapy','Cupping Therapy',1.5, true),
('Craniosacral Therapy','Craniosacral Therapy',2, true),
('Vestibular & Balance Therapy ','Vestibular & Balance Therapy ',1.5, true),
('Soft Tissue Mobilization Techniques','Soft Tissue Mobilization Techniques',1.5, true);


INSERT INTO mrds_user (user_id, user_first_name, user_last_name, user_email, user_mobile, gender, dob, user_created_date, user_modified_date, last_login_at, is_active, user_type_id, profile_image_name, password, user_name, referral_code) VALUES
(1, 'MRDS', 'Admin', 'myreferui@gmail.com', '8879878998', '', '', now(), now(), now(), true, 4, NULL, 'admin@123', 'admin', '');