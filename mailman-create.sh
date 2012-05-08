for domain in \
    lists.fporuba.cz\
    lists.hrbac.cz\
    lists.pudu.cz \
    lists.svetdoma.cz\
    ; do

    sed -r -e "s/^#%%global domain.*$/%global domain $domain/g" mailman.spec > mailman-$domain.spec

    rpmbuild -bs mailman-$domain.spec
done
