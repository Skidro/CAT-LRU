# Create cgroups for cpu modularization
mount -t cgroup xxx /sys/fs/cgroup
mkdir /sys/fs/cgroup/part1
mkdir /sys/fs/cgroup/part2
echo 0-1 > /sys/fs/cgroup/part1/cpuset.cpus
echo 2-11 > /sys/fs/cgroup/part2/cpuset.cpus
