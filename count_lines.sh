git ls-files | grep -P "^(?!tests|experiments|pufferlib/environments).*[^/]+\.([hc])$" | xargs wc -l
git ls-files | grep -P "^(?!tests|experiments|pufferlib/environments).*[^/]+\.py$" | xargs wc -l
git ls-files | grep -P "^(?!tests|experiments|pufferlib/environments).*[^/]+\.pyx$" | xargs wc -l

