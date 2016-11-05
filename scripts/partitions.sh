# Reset the current way partitioning
pqos -R

# Set the number of ways for cache partitions
pqos -e "llc:0=0x003ff;llc:1=0xffc00;"

# Associate cores with partitions
pqos -a "llc:0=0-1;llc:1=2-11;"
