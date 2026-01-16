import streamlit as st
import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
 
st.header("Bar Chart")
 
data = {"a":[23, 12, 78, 4, 54], "b":[0, 13 ,88, 1, 3], 
"c":[45, 2, 546, 67, 56]}
 
df = pd.DataFrame(data)
df
st.bar_chart(data=df)
