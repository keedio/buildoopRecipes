import time,os

ipaserver="ipa01.jcfernandez.cediant.es"
input="/root/hosts_principals.csv"

ts=time.time()

output_dir="/tmp/ambari_kerberos"
generate=open(output_dir+"/generate.sh",'w')
deploy=open(output_dir+"/deploy.sh",'w')

keytabs_dir=output_dir+"/"+str(ts)

keytabsToGen=dict()
with open(input) as f:
    for line in f:
        host,desc,principal,file,directory,owner,group,mode=line.split(',')
        file=directory+'/'+file 
        principal=principal.split('@')[0]
        if not principal in keytabsToGen:
            keytabsToGen[principal]=dict()
        if not host in keytabsToGen[principal]:
            keytabsToGen[principal][host]=dict()
        if not file in keytabsToGen[principal][host]:
            keytabsToGen[principal][host][file]={'owner':owner,'group':group,'mode':mode}

f.close()

help_keytab="/tmp/ambari_kerberos/" + str(ts) + "/help.keytab"
generate.write("mkdir -p %s\n" % keytabs_dir)
for principal in keytabsToGen:
    generate.write("#========================================================\n")
    generate.write("#=====================%s=====================\n" % principal)
    generate.write("#========================================================\n")
    generate.write("rm -f " + help_keytab + "\n")
    if '/' in principal:
        generate.write("ipa service-add %s\n" % principal)
    else:
        generate.write("ipa user-add " + principal + " --first SYSTEM --last SYSTEM\n")
    generate.write("ipa-getkeytab -s %s -p %s -k %s\n" % (ipaserver,principal,help_keytab))
    for host in keytabsToGen[principal]:    
        for file in keytabsToGen[principal][host]:
            generate.write("mkdir -p %s/%s%s\n" % (keytabs_dir,host,os.path.dirname(file)))
            generate.write("ktutil << EOF\n" + 
              "read_kt " + keytabs_dir + "/" + host + file + "\n" + 
              "read_kt " + help_keytab + "\n" +
              "write_kt " + keytabs_dir + "/" + host + file + "\n" +
              "EOF\n")

            file_details=keytabsToGen[principal][host][file]
            owner=file_details['owner']
            group=file_details['group']
            mode=file_details['mode'].replace('\n','')
            deploy.write("ssh " + host + " 'mkdir " + os.path.dirname(file) + "'\n")
            deploy.write("scp " + keytabs_dir + "/" + host + "/" + file + " " + host + ":" + file + "\n")
            deploy.write("ssh " + host + " 'chown " + owner + ":" + group + " " + file + "'\n")
            deploy.write("ssh " + host + " 'chmod " + mode + " " + file + "'\n\n")
generate.close()
deploy.close()

