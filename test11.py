import numpy as np


def 隨機數重置():
    RND1 = np.random.randint(0,1)
    RNDD1 = np.random.randint(0,1)
    RND2 = np.random.randint(0,2)
    RNDD2 = np.random.randint(0,2)
    RND3 = np.random.randint(0,3)
    RNDD3 = np.random.randint(0,3)
    RND4 = np.random.randint(0,4)
    RNDD4 = np.random.randint(0,4)
    RND5 = np.random.randint(0,5)
    RNDD5 = np.random.randint(0,5)
    RND6 = np.random.randint(0,6)
    RNDD6 = np.random.randint(0,6)
    print(f'''隨機數重置 : RND1={RND1},{RNDD1} ; RND2={RND2},{RNDD2} ; RND3={RND3},{RNDD3} ; 
             RND4={RND4},{RNDD4} ; RND5={RND5},{RNDD5} ; RND6={RND6},{RNDD6}''')
    return RND1, RNDD1, RND2, RNDD2


print(隨機數重置())