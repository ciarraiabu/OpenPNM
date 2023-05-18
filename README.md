

## Require Python Packages



## Export PYTHONPATH

    #Clear
    PROJECT_FOLDER=""
    PYTHONPATH=""; export PYTHONPATH;

    AUTO_HOME="/home/dev02/Projects/${PROJECT_FOLDER}"
    PYTHONPATH="${PYTHONPATH}:${AUTO_HOME}:${AUTO_HOME}/lib:${AUTO_HOME}/run:${AUTO_HOME}/tests"
    export PYTHONPATH
    