import streamlit as st
import pandas as pd
import plotly.express as px

# загружаем датасет и удаляем ненужные строки
df_pay = pd.read_excel('tab3_zpl_2023.xlsx', skiprows=4)
payment1 = df_pay.drop(index=[2, 7, 12, 53, 54])

# формируем датасет про Гостиницы и рестораны
pf = payment1.loc[42].values[1:]
nf = pd.DataFrame(pf)
nf.index = range(2017, 2024)
food = pd.DataFrame(nf)
food.rename(columns={0: 'Гостиницы и рестораны'}, inplace=True)

# формируем датасет про образование
pf1 = payment1.loc[50].values[1:]
nf1 = pd.DataFrame(pf1)
nf1.index = range(2017, 2024)
food1 = pd.DataFrame(nf1)
food1.rename(columns={0: 'Образование'}, inplace=True)

# формируем датасет про здравоохранение
pf2 = payment1.loc[51].values[1:]
nf2 = pd.DataFrame(pf2)
nf2.index = range(2017, 2024)
food2 = pd.DataFrame(nf2)
food2.rename(columns={0: 'Здравоохранение и предоставление социальных услуг'}, inplace=True)

payment2 = pd.read_excel('tab3_zpl_2023.xlsx', sheet_name='2000-2016 гг.',skiprows=2)
payment2 = payment2.drop(index=[4, 8, 35, 36]).reset_index(drop=True)

lf1 = payment2[payment2['  Профессии']=='Гостиницы и рестораны']
df = pd.DataFrame(lf1.T).drop('  Профессии')
df.rename(columns={24: 'Гостиницы и рестораны'}, inplace=True)
df = pd.concat([df,food])

nf1 = payment2[payment2['  Профессии']=='Образование']
nf = pd.DataFrame(nf1.T).drop('  Профессии')
nf.rename(columns={30: 'Образование'}, inplace=True)
nf = pd.concat([nf, food1])

mf1 = payment2[payment2['  Профессии']=='Здравоохранение и предоставление социальных услуг']
mf = pd.DataFrame(mf1.T).drop('  Профессии')
mf.rename(columns={31: 'Здравоохранение и предоставление социальных услуг'}, inplace=True)
mf = pd.concat([mf, food2])
df_new = pd.concat([df, nf, mf ], axis="columns", join='outer')

infl = pd.read_excel('Ipc_mes_07-2024.xlsx', skiprows=3)
infl = infl.drop(index=[0,13,14,15,16,17])
infl = infl.reset_index(drop=True)

infl_new = infl.iloc[::, 10:34].mean()

years = df_new.T.columns[0:].astype(int)

paycheck1 = df_new['Гостиницы и рестораны'].values[0:]
paycheck2 = df_new['Образование'].values[0:]
paycheck3 = df_new['Здравоохранение и предоставление социальных услуг'].values[0:]

infl = pd.read_excel('Ipc_mes_07-2024.xlsx', skiprows=3)
infl = infl.drop(index=[0, 13, 14, 15, 16, 17])
infl = infl.reset_index(drop=True)


df_inf1 = df_new['Гостиницы и рестораны']*infl_new
d1 = pd.DataFrame(df_inf1)
df_inf2 = df_new['Образование']*infl_new
d2 = pd.DataFrame(df_inf2)
df_inf3 = df_new['Здравоохранение и предоставление социальных услуг']*infl_new
d3 = pd.DataFrame(df_inf3)
d3.rename(columns={0:'Здравоохранение и предоставление социальных услуг'}, inplace=True)
d2.rename(columns={0:'Образование'}, inplace=True)
d1.rename(columns={0:'Гостиницы и рестораны'}, inplace=True)
df_inf = pd.concat([d1, d2, d3], axis="columns", join='outer')

df3 = pd.read_excel('S_prs_2023.xlsx', skiprows=3, sheet_name='2')
df3 = df3.drop(index=[96,97]).reset_index(drop=True)

df5 = pd.read_excel('05-05_2017-2023.xls', sheet_name='Лист2', skiprows=2)
df5 = df5.drop(index=[0,1]).reset_index(drop=True)

gost = pd.DataFrame(df5.loc[8])
gost.rename(columns={8:'Гостиницы и рестораны'}, inplace=True)
gost = gost.drop('Профессии')
x1 = gost.values[1:]

obr = pd.DataFrame(df5.loc[16])
obr.rename(columns={16:'Образование'}, inplace=True)
obr = obr.drop('Профессии')
x2 = obr.values[1:]

zd = pd.DataFrame(df5.loc[17])
zd.rename(columns={17:'Здравоохранение и предоставление социальных услуг'}, inplace=True)
zd = zd.drop('Профессии')
x3 = zd.values[1:]

data_new = pd.concat([gost, obr, zd ], axis="columns", join='outer')

def page_1():
    st.title('Cтатистика зарплат России')
    st.write('')
    st.write(
        """Данное приложение предназначено для того, чтобы показать динамику изменения зарплат и  занятости 
        в выбранных мною 3-х областях. Первым шагом будет построение графика измненения зарплат"""
    )
    st.text('Данные о зарплатах по видам экономической деяельности за 2000-2023 год')
    st.dataframe(df_pay)
    st.dataframe(df_new)
    st.write(
        """Данный график показывает положительную динамику роста зарплат в представленных видах 
        деятельности за исключением некоторых небольших отрезков времени"""
    )
    st.line_chart(df_new[['Гостиницы и рестораны', 'Образование', 'Здравоохранение и предоставление социальных услуг']])
    placeholder = st.empty()
    if st.button("Зарплаты с учетом инфляции", on_click=page_2, key="static2"):
        placeholder.empty()  # Очистить предыдущее содержимое
        #st.rerun()# Перезапустить
    if st.button("Занятость России", on_click=page_3, key="static4"):
        placeholder.empty()


def page_2():
    st.title('Cтатистика зарплат России c учетом инфляции')
    st.dataframe(infl_new)
    st.write(
        """Посмотрим как выглядит график изменения индекса инфляции по годам"""
    )
    plot = px.line(infl_new)
    st.plotly_chart(plot)
    st.write(
        """Данные показывают, что индекс инфляции изменялся небольшими скачками за период от 2000 до 2023 года.
        Минимальное значение наблюдается в 2017 году с дальнейшим скачом в 2022 году."""
    )
    st.write('')
    st.write(
        """Теперь построим график зарплат выбранных 3-х сфер, учитывая индекс инфляции"""
    )
    st.dataframe(df_inf)
    st.line_chart(df_inf[['Гостиницы и рестораны', 'Образование', 'Здравоохранение и предоставление социальных услуг']])
    st.write(
        """Глядя на данный график можно сделать вывод, что инфляция особо
         не повлияла на динамику изменения зарплат в выбранных сферах"""
    )
    st.write('')
    placeholder = st.empty()
    if st.button("Зарплаты России", on_click=page_1, key="static"):
        placeholder.empty()
        #st.rerun()
    if st.button("Занятость России", on_click=page_3, key="static3"):
        placeholder.empty()


def page_3():
    st.title('Cтатистика занятости России по выбранным областям')
    st.write('')
    st.write(
        """Здесь предоставлен датасет с данными об уровне занятости в России (в процентах) по выбранным областям"""
    )
    st.write('')
    st.dataframe(data_new)
    st.write('')
    st.write(
        """Теперь построим график уровня занятости"""
    )
    plot1 = px.line(data_new[['Гостиницы и рестораны', 'Образование', 'Здравоохранение и предоставление социальных услуг']])
    st.plotly_chart(plot1)
    st.write('')
    st.write(
        """Исходя из графика можно сделать вывод, что занятость в сфере образования понизилась за последние 6 лет,
        в то время как та же величина для гостиничного бизнеса увеличилась. Показатели в сфере здравоохранения 
        относительно не изменились за выбранный период."""
    )

    values = [x1, x2, x3]
    unemployment1 = df3.loc[0].values[1:]
    unemployment = pd.DataFrame(unemployment1)
    app = []
    for i in range(len(values)):
        new = pd.DataFrame(values[i])
        correlation = new[0].corr(unemployment[0])
        app.append(correlation)

    options = {'Гостиницы и рестораны': app[0], 'Образование': app[1],
               'Здравоохранение и предоставление социальных услуг': app[2]}


    st.write('')
    st.write('Корреляция безработицы в России и уровня занятости в сфере гостиницы и рестораны составляет:',
             options['Гостиницы и рестораны'])
    st.write('')
    st.write('Корреляция безработицы в России и уровня занятости в сфере образования составляет:',
             options['Образование'])
    st.write('')
    st.write('Корреляция безработицы в России и уровня занятости в сфере здравооохранения составляет:',
             options['Здравоохранение и предоставление социальных услуг'])
    placeholder = st.empty()
    if st.button("Зарплаты России", on_click=page_1, key="static5"):
        placeholder.empty()
    if st.button("Зарплаты с учетом инфляции", on_click=page_2, key="static6"):
        placeholder.empty()


def main():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Cтатистика зарплат России'
        page_1()
    elif st.session_state.current_page == 'Cтатистика зарплат России c учетом инфляции':
        page_2()

    elif st.session_state.current_page == 'Cтатистика занятости России по выбранным областям':
        page_3()



if __name__ == "__main__":
    main()