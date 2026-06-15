ALTER DATABASE thscoreboard OWNER TO thscoreboard;
ALTER USER thscoreboard CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE thscoreboard TO thscoreboard;
GRANT USAGE, CREATE ON SCHEMA public TO thscoreboard;
