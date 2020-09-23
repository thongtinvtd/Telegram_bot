function getHeaderInfo()
{
	contentloader("HMI.ChbInfo.EquipmNo", "EquipmNo");
	contentloader("P_X7IPaddr", "IpAdr");
}

function getChbInfo()
{
	var str = "";
	var val = 0;
	var PGNr = 0;
	var PGStat = 0;
	var ErrStat = 0;
	var ChbStat = "";
	var ChbMode = "";
	var ImgSrc = "";
	var ImgSrcMS = "";

	str = getHMIValue("HMI.Prog.ProfileNo");
	PGNr = parseInt(str);
	if (PGNr >0)
	{
		str = getHMIValue("HMI.Prog.ProfileName");
		ChbMode = "AUTO:" + str;
	
		str = getHMIValue("HMI.Prog.Status");
		PGStat = parseInt(str.substr(3), 16);
	
		if (PGStat & 1)
		{
			ImgSrc = "../image/run.gif";
			ChbStat = "RUNNING";
		}
		if (PGStat & 2)
		{
			ImgSrc = "../image/on_Pause.gif";
			ChbStat = "PAUSED";
		}
		if (PGStat & 4)
		{
			ImgSrc = "../image/on_Wait.gif";
			ChbStat = "WAITING";
		}
		if (PGStat & 16)
		{
			ImgSrc = "../image/on_Delay.gif";
			ChbStat = "WAITING FOR START";
			str = getHMIValue("HMI.Prog.ProgName[" + PGNr + "]");
			ChbMode = "AUTO:" + str;
		}
	}
	else
	{
		ChbMode = " ";
		str = getHMIValue("HMI.ChbStatus.StartMode");
		val = parseInt(str.substr(3), 16);
		if (val > 0)
		{
			ChbMode = "MANUAL";
			ImgSrc = "../image/run.gif";
			ChbStat = "RUNNING";
		}
		else
		{
			ChbMode = " ";
			ImgSrc = "../image/on_00.gif";
			ChbStat = "OFF";
		}
	}

	str = getHMIValue("HMI.MS_AnyDW");
	ErrStat = parseInt(str.substr(3), 16);
	if (ErrStat == 0)
	{
		ImgSrcMS = "../image/on_00.gif";
	}
	else
	{
		if (ErrStat & (1 << 16))
		{
			ImgSrcMS = "../image/ms_alarm.png";
			ChbMode = "ERRORS";
//			$("#MsImg").after("<a href='../warning/c3kwarn.plc'>");
		} else 
		if (ErrStat & (1 << 17)) 
		{
			ImgSrcMS = "../image/ms_warn.png";
			ChbMode = "WARNINGS";
//			$("#MsImg").after("<a href='../warning/c3kwarn.plc'>");
		} else 
		if (ErrStat & (1 << 18)) 
		{
			ImgSrcMS = "../image/ms_info.png";
			ChbMode = "INFOS";
//			$("#MsImg").after("<a href='../warning/c3kwarn.plc'>");
		}
	}


	
	$("#ChbMode").text(ChbMode);
	// $("#ChbStatus").text(ChbStat);
	$("#StatImg").attr("src", ImgSrc);
	$("#MsImg").attr("src", ImgSrcMS);

	setTimeout(getChbInfo, 5000);
}

function getHMIValue(dataid) {
	var ret;
	
	$.ajax({
		url: "../macros/getHMIvar.plc?plc_var_name=" + dataid,
		async: false,
		method: 'GET',
			timeout: (10 * 1000),
			error: function( objAJAXRequest, strError ){
				ret = "Error! " +  strError;
//				alert("Error! " +  strError);
			},
		success: function(msg){
//				ret = msg;
				ret = msg.replace(/\"/g, "");

		 }
	});
	
	return (ret);
}

function setHMIValue(dataid, value) {
	var ret;
	
	$.ajax({
		url: "../macros/tag_write.plc?target_symbol=local&tag_name=" + dataid + "&tag_value=" + value,
		async: true,
		method: 'GET',
			timeout: (10 * 1000),
			error: function( objAJAXRequest, strError ){
				ret = "Error! " +  strError;xi
			},
		success: function(msg){
				ret = msg;
		 }
	});
	
	return (ret);
}

function contentloader(dataid, target) {
		var msgneu;
		$.ajax({
			url: "../macros/getHMIvar.plc?plc_var_name=" + dataid,
			async: false,
			method: 'GET',
				timeout: (10 * 1000),
				error: function( objAJAXRequest, strError ){
					$("#" + target).text("Error! " +  strError);
				},
			success: function(msg){
				msgneu = msg.replace(/\"/g, "");
//				$("#" + target).text(msgneu);
				$("#" + target).html(msgneu);
			 }
		});
}

function myPrint(str) 
{
	var i;
	var len;
	var filterstr = "";
	var code;

	len = str.length;
	for (i=0; i<len ; i++)
	{
		if (str.charAt(i) != "\"")
		{
/*		
			code = str.charCodeAt(i);
			if (code == 65533)
				filterstr = filterstr + "&deg;";
			else
*/			
				filterstr = filterstr + str.charAt(i);
		}
	}
//  document.charset = "iso-8859-1";
//  document.open();
  document.write(filterstr);
//  document.close();
}
