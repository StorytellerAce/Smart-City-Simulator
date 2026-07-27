using UnityEngine;

[CreateAssetMenu(menuName = "Settings/Game Settings")]
public class Settings : ScriptableObject
{
    // General settings
    [SerializeField] private string baseUrl = "http://localhost:8000";
    [SerializeField] private string baseWsUrl = "ws://localhost:8000/ai/ws";

    // Game Settings
    [SerializeField] private int generateReactionTurn = 3;
    [SerializeField] private int generateAdviceTurns = 5;
    [SerializeField] private int generateObjectiveTurn = 16;
    [SerializeField] private int endTurnCount = 21;

    [SerializeField] private int gridWidth = 80;
    [SerializeField] private int gridHeight = 80;

    // Game Initialization Settings
    [SerializeField] private int initialAP = 3;
    [SerializeField] private int maxAP = 3;
    [SerializeField] private int initialGold = 4000;
    [SerializeField] private Vector3Int townHallPosition = new Vector3Int(10, 1, 0);
    [SerializeField] private float populationLimiterThreshold = 2.5f; // for removing ReachPopulation objective if too crazy

    // Public read-only properties
    public string BaseUrl => baseUrl;
    public string BaseWsUrl => baseWsUrl;

    public int GenerateReactionTurn => generateReactionTurn;
    public int GenerateAdviceTurns => generateAdviceTurns;
    public int GenerateObjectiveTurn => generateObjectiveTurn;
    public int EndTurnCount => endTurnCount;

    public int GridWidth => gridWidth;
    public int GridHeight => gridHeight;

    public int InitialAP => initialAP;
    public int MaxAP => maxAP;
    public int InitialGold => initialGold;
    public Vector3Int TownHallPosition => townHallPosition;
    public float PopulationLimiterThreshold => populationLimiterThreshold;
}