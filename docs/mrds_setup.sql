USE mrds_v1;
SET FOREIGN_KEY_CHECKS=0;
#truncate user;

truncate user_type;
INSERT INTO `user_type`
(
`user_type_id`,
`user_type`,
`is_active`)
VALUES
('1', 'Patient', 1),
('2', 'PT',1),
('3', 'DR', 1),
('4', 'Admin', 1);

truncate specialization;
INSERT INTO `specialization`
(
`specialization`,
`keywords`,
`user_type_id`,
`is_active`)
VALUES
('Orthopaedic','Orthopaedic',2,1),
('Sports','Sports',2,1),
('Rehabilitation','Rehabilitation',2,1),
('Post fracture stiffness','Post fracture stiffness',2,1),
('Joint pain','Joint pain',2,1),
('Gout','Gout',2,1),
('Tennis elbow','Tennis elbow',2,1),
('Stroke CVA','Stroke CVA',3,1),
('Neuro','Neuro',3,1),
('Nerve root  compression','Nerve root  compression',3,1),
('Spinal cord injury','Spinal cord injury',3,1),
('Multiple sclerosis','Multiple sclerosis',3,1),
('Sciatica','Sciatica',3,1),
('Delayed milestones with Motor control','Delayed milestones with Motor control',3,1),
('Ataxia','Ataxia',3,1),
('Antonia','Antonia',3,1);


truncate qualification;
INSERT INTO `qualification`
(
`qualification`,
`keywords`,
`user_type_id`,
`is_active`)
VALUES
('BPT','BPT',2,1),
('MPT','MPT',2,1),
('MBBS','MBBS',3,1),
('D Ortho','D Ortho',3,1),
('MD','MD',3,1);


truncate subscription;
INSERT INTO `subscription`
(
`subscription_name`,
`subscription_details`,
`subscription_validity`,
`cost`,
`is_active`,
`user_type_id`)
VALUES
('One-Month','1 Month',1, 100, 1, 1),
('Six-Month','6 Month',6, 500, 1, 1),
('One-Year','1 Year',12, 800, 1, 1),
('One-Month','1 Month',1, 200, 1, 2),
('Six-Month','6 Month',6, 1000, 1, 2),
('One-Year','1 Year',12, 1600, 1, 2),
('One-Month','1 Month',1, 300, 1, 3),
('Six-Month','6 Month',6, 1500, 1, 3),
('One-Year','1 Year',12, 2500, 1, 3);



truncate package;
INSERT INTO `package`
(
`package_name`,
`details`,
`cost`,
`is_active`)
VALUES
('Spinal pain (neck/back) without nerve compression ','Spinal pain (neck/back) without nerve compression ',1, 1),
('Spinal pain (neck/back) with nerve compression ','Spinal pain (neck/back) with nerve compression ',1.25, 1),
('Needle Therapy','Needle Therapy',2, 1),
('Cupping  Therapy','Cupping Therapy',1.5, 1),
('Craniosacral Therapy','Craniosacral Therapy',2, 1),
('Vestibular & Balance Therapy ','Vestibular & Balance Therapy ',1.5, 1),
('Soft Tissue Mobilization Techniques','Soft Tissue Mobilization Techniques',1.5, 1);


INSERT INTO `user` (`user_id`, `user_first_name`, `user_last_name`, `user_email`, `user_mobile`, `gender`, `dob`, `user_created_date`, `user_modified_date`, `last_login_at`, `is_active`, `user_type_id`, `profile_image_name`, `password`, `user_name`, `referral_code`) VALUES
(1, 'MRDS', 'Admin', 'myreferui@gmail.com', '8879878998', '', '', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000', '0000-00-00 00:00:00.000000', 1, 4, NULL, 'admin@123', 'admin', '');