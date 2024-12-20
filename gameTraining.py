import gymnasium as gym
import os 
import gameEnvironment
from stable_baselines3 import A2C

move = {
    0:"Up",
    1:"Down",
    2:"Left",
    3:"Right",
}

def stable3_train(render=False):

    model_dir = 'models'
    logs_dir = 'logs'

    os.makedirs(model_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    env = gym.make('2048', render_mode='human' if render else None, seed = 42)

    model = A2C('MlpPolicy', env, learning_rate=0.00001, verbose=0, device='cpu', tensorboard_log=logs_dir)
   
    # This loop will keep training until you stop it with Ctr-C.
    # Start another cmd prompt and launch Tensorboard: tensorboard --logdir logs
    # Once Tensorboard is loaded, it will print a URL. Follow the URL to see the status of the training.
    # Stop the training when you're satisfied with the status.
    TIMESTEPS = 1000
    iters = 0
    for _ in range(10000):
        iters += 1
        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False) # train
        if iters%50==0:
            model.save(f"{model_dir}/a2c_{iters}_v0") # Save a trained model every TIMESTEPS
        if iters%10==0:
            print(f"{iters} completed")



def test_sb3(model_path:str, render=True):

    env = gym.make('2048', render_mode='human' if render else None)

    # Load model
    model = A2C.load(model_path, env=env)

    # Run a test
    obs = env.reset()[0]
    terminated = False
    for i in range(10000):
        action, _ = model.predict(observation=obs, deterministic=False) 
        print(move[int(action)])
        obs, _, terminated, _, _ = env.step(action)

        if terminated:
            print("GAME OVER\n"*10)
            print(i)
            break



if __name__ == "__main__":

    # For training
    # stable3_train()

    # For testing
    test_sb3("models/a2c_700_v0", render=True)
