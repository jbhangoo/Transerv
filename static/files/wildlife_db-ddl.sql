-- "role" definition

CREATE TABLE role (
	id INTEGER NOT NULL, 
	name VARCHAR(20) NOT NULL, 
	level INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (level)
);


-- site definition

CREATE TABLE site (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(100), 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (description)
);


-- species definition

CREATE TABLE species (
	id INTEGER NOT NULL, 
	species_code VARCHAR(10) NOT NULL, 
	common_name VARCHAR(100) NOT NULL, 
	scientific_name VARCHAR(100), 
	rarity INTEGER, 
	status BOOLEAN, 
	comments TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (common_name), 
	UNIQUE (scientific_name)
);

CREATE UNIQUE INDEX ix_species_species_code ON species (species_code);


-- geography definition

CREATE TABLE geography (
	id INTEGER NOT NULL, 
	site_id INTEGER, 
	geodetic_system VARCHAR(100), 
	latitude FLOAT, 
	longitude FLOAT, 
	northing FLOAT, 
	easting FLOAT, 
	zone INTEGER, 
	band VARCHAR(1), 
	PRIMARY KEY (id), 
	FOREIGN KEY(site_id) REFERENCES site (id)
);


-- project definition

CREATE TABLE project (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description VARCHAR(100), 
	species_id INTEGER NOT NULL, 
	is_active BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (description), 
	FOREIGN KEY(species_id) REFERENCES species (id)
);


-- project_site definition

CREATE TABLE project_site (
	id INTEGER NOT NULL, 
	project_id INTEGER, 
	site_id INTEGER, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES project (id), 
	FOREIGN KEY(site_id) REFERENCES site (id)
);


-- "user" definition

CREATE TABLE user (
	id INTEGER NOT NULL, 
	role_id INTEGER, 
	created_at DATETIME, 
	username VARCHAR(100) NOT NULL, 
	password_hash VARCHAR(256) NOT NULL, 
	name VARCHAR(100), 
	email VARCHAR(100), 
	is_active BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES role (id), 
	UNIQUE (username)
);


-- survey definition

CREATE TABLE survey (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	project_id INTEGER, 
	site_id INTEGER, 
	survey_date DATE NOT NULL, 
	time_start TIME, 
	time_end TIME, 
	observer_count INTEGER, 
	comments TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(project_id) REFERENCES project (id), 
	FOREIGN KEY(site_id) REFERENCES site (id)
);


-- observation definition

CREATE TABLE observation (
	id INTEGER NOT NULL, 
	survey_id INTEGER, 
	species_id INTEGER, 
	count INTEGER, 
	count_supplemental INTEGER, 
	latitude FLOAT, 
	longitude FLOAT, 
	direction VARCHAR(5), 
	behavior VARCHAR(50), 
	comments TEXT, 
	created_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(survey_id) REFERENCES survey (id), 
	FOREIGN KEY(species_id) REFERENCES species (id)
);