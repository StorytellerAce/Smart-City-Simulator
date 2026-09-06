using UnityEngine;
using UnityEngine.SceneManagement;

public class StartGameSceneManager : MonoBehaviour
{
    private string MainSceneName = SceneName.MainScene.ToString();

    public void PlayGame(){
        SceneManager.LoadSceneAsync(MainSceneName); 
    }

    public void QuitGame(){
        Logger.Log("Quitting the game...");  
        Application.Quit();
    }
}
