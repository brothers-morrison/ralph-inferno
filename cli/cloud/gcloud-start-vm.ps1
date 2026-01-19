Param(
	# Key = instance name, Value = zone
	[hashtable]$Vm_List = @{"ralph-sandbox"="us-central1-a"}, #us-west1-a
	# [start,stop,create]
	[string] $Action = "stop",
	$NewVM_Zone = "us-central1-a",
	$Img_Family = "ubuntu-2204-lts",
	$Img_Project = "ubuntu-os-cloud",
	$Disk_Size = "10GB",
	$Allow_Ports = @{
		"80"="http"
		"443"="https"
	},
	$color_warn = "Yellow",
	$color_error = "Red",
	$color_good = "Green"
)

# TURN OFF BEFORE GOING TO PROD
# Lets use this guy's tracing code
. ./trace.ps1
#Set-PSDebug -Trace 1
#Set-PSDebug -Step

if(-Not($Action))
{
	Write-Host "-Action is required: [start,stop,create]"
	Exit
}


<#
.SYNTAX
	Source - https://stackoverflow.com/a
	Posted by iRon, modified by community. See post 'Timeline' for change history
	Retrieved 2026-01-18, License - CC BY-SA 4.0
#>
Function IIf($If, $Then, $Else) {
    If ($If -IsNot "Boolean") {$_ = $If}
    If ($If) {If ($Then -is "ScriptBlock") {&$Then} Else {$Then}}
    Else {If ($Else -is "ScriptBlock") {&$Else} Else {$Else}}
}



Function Begin_SSH_Session($VmName = "ralph-sandbox", $VmZone = "us-central1-a")
{
	gcloud compute ssh $VmName --zone=$VmZone
}

Function Start_VMs([hashtable]$Vm_List)
{
	# Simple version - auto-detects zones
	$gcloud_instances = gcloud compute instances list --format=json | ConvertFrom-Json
	$instanceMap = @{}
	$gcloud_instances | ForEach-Object { $instanceMap[$_.name] = $_.zone.Split('/')[-1] }

	foreach ($vm in $Vm_List.Keys) {
		if ($instanceMap.ContainsKey($vm)) {
			$zone = $instanceMap[$vm];
			Write-Host "Starting $vm in $zone..." -ForegroundColor $color_warn
			gcloud compute instances start $vm --zone=$zone --quiet
		} else {
			Write-Host "Instance $vm not found!" -ForegroundColor $color_error
		}
	}
}
if("start" -eq $Action){
	Start_VMs -Vm_List:$Vm_List
	Begin_SSH_Session
}


Function Create_VM(
	$VmName = "ralph-sandbox",
	$NewVM_Zone = "us-central1-a",
	$Img_Family = "ubuntu-2204-lts",
	$Img_Project = "ubuntu-os-cloud",
	$Disk_Size = "10GB"
	)
{

# RULE OF THUMB FOR "RIGHT-SIZING" for Ubuntu 22 : 10GB
	# Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1045-gcp x86_64)
	# Filesystem      Size  Used Avail Use% Mounted on
	# /dev/root       9.6G  4.7G  4.9G  49% /
# At this time 2026-Jan-18, Version: "Ubuntu 22.04.5 LTS" is around 4.7GB on a vanilla VM from gcloud
Assumptions = @{
	"OS@Ubu22" : "4.7G"
	"LogsAndNormalGrowth" : "10%"
	"GitProjectFilesSize + DatabaseSize" : "s"
	"DatabaseExpectedGrowthRate" : "r"
	"Total_Need_Equation" : "Need = (OS + s) + ((OS + s) * 10%)"
	"TotalNeed" 	: "N = (4.7G + s) 	+ ((4.7G + s) * 0.1)"
	"ThumbSizes01" 	: "N = (4.7G + 1)   + ((4.7G + 1) * 0.1)...    	N = 6.3 GB"
	"ThumbSizes10" 	: "N = (4.7G + 10)  + ((4.7G + 10) * 0.1)...		N = 16  GB"
	"ThumbSizes100"	: "N = (4.7G + 100) + ((4.7G + 100) * 0.1)...	N = 115 GB"
}
# TBD: get the size of the git project in order to "right-size" the disk needed
# Side note: most GIT repos have a size limit of... 10GB, and individual files/push limits at 2GB
# https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits

	# Create VM instance
	gcloud compute instances create $VmName			`
		--zone="$NewVM_Zone" 						`
		--machine-type=n1-standard-1 				`
		--image-family="$Img_Family" 				`
		--image-project="$Img_Project" 				`
		--boot-disk-size="$Disk_Size" 				`
		--boot-disk-type=pd-standard 				`
		--tags=http-server
}

if("create" -eq $Action){
	foreach ($vm in $Vm_List.Keys){
	 Create_VM `                     	`
		-VmName = $vm,            		`
		-NewVM_Zone = $Vm_List[$vm], 	`
		-Img_Family = $Img_Family,   	`
		-Img_Project = $Img_Project, 	`
		-Disk_Size = $Disk_Size      	    
	}


	Function set_firewall_rules($Allow_Ports)
	{
		foreach($port in $Allow_Ports)
		{
			Write-Host "$($port.Name) : $($port.Value)"
			gcloud compute firewall-rules create "default-allow-$($port.Value)"		`
				--allow=tcp:$($port.Name)											`
				--target-tags="$($port.Value)-server"

			# firewall : ALLOW HTTPS
			#gcloud compute firewall-rules create default-allow-https `
			#	--allow=tcp:443 `
			#	--target-tags=https-server
		}
	}

	#set_firewall_rules($Allow_Ports)

}



Function Stop_VMs(
		$color_title = "Cyan",
		$color_warn = "Yellow",
		$color_good = "Green")
{

	Write-Host "Attempting to Stop all GCP compute instances..." -ForegroundColor $color_title

	$instances = gcloud compute instances list --format=json | ConvertFrom-Json

	$instances

	# Split-Path "zone" -Leaf
	$instances | Select-Object STATUS,Name, `
		@{Name = 'Zone'; Expression = { Split-Path $_.Zone -Leaf;}},
		@{Name = 'EXTERNAL_IP'; Expression = { $_.networkInterfaces.accessConfigs.natIP }} | Format-Table -autosize

	foreach ($instance in $instances) {
		if ($instance.status -eq "RUNNING") {
			$name = $instance.name
			$zone = $instance.zone.Split('/')[-1]
			
			Write-Host "Stopping: $name in $zone" -ForegroundColor $color_warn
			gcloud compute instances stop $name --zone=$zone --quiet
		}
	}

	Write-Host "All instances stopped!" -ForegroundColor $color_good
}

if("stop" -eq $Action){
	Stop_VMs
}