using System;
using System.IO;
using UnityEngine;
using UnityEngine.Networking;

public static partial class CloudAPI
{
	public static void CheckVersion(Action<LoginResponse> response)
	{
		GameHandler.AddStatus<QueryingGameTimeStatus>(new QueryingGameTimeStatus());

		string filePath = Path.Combine(Application.dataPath, "..", "Kirigiri", "server.txt");
		string text;

		try
		{
			text = File.ReadAllText(filePath).Trim();
		}
		catch (Exception e)
		{
			Debug.LogError("Failed to read server.txt: " + e.Message);
			GameHandler.ClearStatus<QueryingGameTimeStatus>();
			return;
		}

		Debug.Log("Sending GET Request to: " + text);
		UnityWebRequest request = UnityWebRequest.Get(text);
		request.SendWebRequest().completed += delegate (AsyncOperation _)
		{
			GameHandler.ClearStatus<QueryingGameTimeStatus>();
			if (request.result != UnityWebRequest.Result.Success)
			{
				Debug.Log("Got error: " + request.error);
				if (request.result != UnityWebRequest.Result.ConnectionError)
				{
					response?.Invoke(new LoginResponse
					{
						VersionOkay = true,
						HoursUntilLevel = 1337,
						MinutesUntilLevel = 1337,
						SecondsUntilLevel = 1337,
						Message = "Thank you for playing PEAK! Pro tip, tapping SPRINT while climbing makes you do a LUNGE!"
					});
				}
				return;
			}

			string responseText = request.downloadHandler.text;
			Debug.Log("Got message: " + responseText);
			LoginResponse loginResponse = JsonUtility.FromJson<LoginResponse>(responseText);
			response?.Invoke(loginResponse);
		};
	}
}
