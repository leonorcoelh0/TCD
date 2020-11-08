def plot_features_3d(features,cols,title):
    fig = px.scatter_3d(features, x=cols[0], y=cols[1], z=cols[2], color=features['Label Name'], title=title,
                       color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_traces(marker=dict(size=4))
    fig.show() 
    
def plot_features_2d(features,cols,title):
    fig = px.scatter(features, x=cols[0], y=cols[1], color=features['Label Name'], title=title,
                       color_discrete_sequence=px.colors.qualitative.Light24)
    fig.update_traces(marker=dict(size=3))
    fig.show() 

f1 = 'Acc AVG'
f2 = 'Acc EVA Gravity'
f3=''
# f3 = 'Acc Z Spec Ent'

if(f3 == ''):
    title_2d = f1 + ' vs ' + f2
    cols_2d = [f1,f2]
    plot_features_2d(features,cols_2d,title_2d)
else:
    title_3d = f1 + ' vs ' + f2 + ' vs ' + f3
    cols_3d = [f1,f2,f3]
    plot_features_3d(features,cols_3d,title_3d)