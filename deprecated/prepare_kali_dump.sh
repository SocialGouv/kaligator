DUMP_DIR=$1
rm -r $DUMP_DIR/flattened
mkdir -p $DUMP_DIR/flattened/articles
mkdir -p $DUMP_DIR/flattened/conteneurs
mkdir -p $DUMP_DIR/flattened/section_tas
mkdir -p $DUMP_DIR/flattened/textes

mkdir -p $DUMP_DIR/merged

# TODO : fix using $DUMP_DIR in sh -c command
find $DUMP_DIR/global/article -type f -exec sh -c 'cp "$@" raw-data/kali/kali/flattened/articles' _ {} +
find $DUMP_DIR/global/conteneur -type f -exec sh -c 'cp "$@" raw-data/kali/kali/flattened/conteneurs' _ {} +
find $DUMP_DIR/global/section_ta -type f -exec sh -c 'cp "$@" raw-data/kali/kali/flattened/section_tas' _ {} +
find $DUMP_DIR/global/texte -type f -exec sh -c 'cp "$@" raw-data/kali/kali/flattened/textes' _ {} +

# merge all xmls into a single one
find $DUMP_DIR/flattened/articles -name "*.xml" -print0 | xargs -0 cat > $DUMP_DIR/merged/articles.xml

# remove duplicate <?xml header lines
sed -i '/^<?xml / d' $DUMP_DIR/merged/articles.xml

sed -i '1s;^;<?xml version="1.0" encoding="UTF-8"?>;' $DUMP_DIR/merged/articles.xml
